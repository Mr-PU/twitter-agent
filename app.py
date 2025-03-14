import streamlit as st
import tweepy
import time
import threading
import logging
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import os
import openai
import queue

# Load environment variables
load_dotenv()

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure logging
logging.basicConfig(
    filename='twitter_agent.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Twitter API credentials from .env
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Authenticate with Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Predefined tweet source
TWEET_FILE = "tweets.txt"

# CrewAI Agents with OpenAI integration
tweet_writer = Agent(
    role='Tweet Writer',
    goal='Generate engaging and concise tweets under 280 characters.',
    backstory='A creative writer skilled in crafting short, impactful messages.',
    verbose=True,
    llm="gpt-4o-mini"
)

tweet_editor = Agent(
    role='Tweet Editor',
    goal='Refine tweets for clarity and engagement.',
    backstory='An editor with a keen eye for detail and audience appeal.',
    verbose=True,
    llm="gpt-4o-mini"
)

def load_tweets_from_file():
    """Load predefined tweets from a file."""
    try:
        with open(TWEET_FILE, 'r') as file:
            tweets = [line.strip() for line in file if line.strip()]
        return tweets
    except FileNotFoundError:
        logging.error(f"Tweet file {TWEET_FILE} not found.")
        return []

def generate_ai_tweet(prompt=None, message_queue=None, refine=True):
    """Generate a tweet using CrewAI agents with OpenAI."""
    try:
        if prompt:
            write_description = f'Generate a creative tweet under 280 characters based on this prompt: "{prompt}".'
            edit_description = f'Refine the tweet based on this prompt: "{prompt}" for clarity and engagement.'
        else:
            write_description = 'Generate a creative tweet under 280 characters.'
            edit_description = 'Refine the tweet for clarity and engagement.'

        write_task = Task(
            description=write_description,
            agent=tweet_writer,
            expected_output='A concise, engaging tweet (max 280 characters).'
        )
        
        tasks = [write_task]
        if refine:
            edit_task = Task(
                description=edit_description,
                agent=tweet_editor,
                expected_output='A polished tweet ready for posting (max 280 characters).'
            )
            tasks.append(edit_task)

        crew = Crew(
            agents=[tweet_writer] + ([tweet_editor] if refine else []),
            tasks=tasks,
            process=Process.sequential
        )
        
        crew.kickoff()
        tweet_content = tasks[-1].output
        
        if refine and message_queue:
            message_queue.put({"type": "preview", "content": f"Next tweet: {tweet_content}"})
        
        return tweet_content
    except Exception as e:
        logging.error(f"Error in CrewAI tweet generation: {e}")
        fallback_message = "Stay tuned for more updates! #TwitterBot"
        if refine and message_queue:
            message_queue.put({"type": "preview", "content": f"Next tweet: {fallback_message}"})
        return fallback_message

def post_tweet(content):
    """Post a tweet to Twitter."""
    if len(content) > 280:
        logging.error(f"Tweet exceeds 280 characters: {content}")
        return False, f"Error: Tweet exceeds 280 characters ({len(content)} chars)"
    try:
        api.update_status(content)
        logging.info(f"Successfully posted tweet: {content}")
        return True, f"Tweet posted: {content}"
    except tweepy.TweepyException as e:
        logging.error(f"Failed to post tweet: {e}")
        return False, f"Error: {e}"

def twitter_agent(interval, use_ai, stop_event, prompt=None, message_queue=None):
    """Main agent loop to post tweets at regular intervals with preview."""
    logging.info("Twitter Posting Agent started.")
    
    tweets = load_tweets_from_file()
    tweet_index = 0
    
    while not stop_event.is_set():
        if use_ai:
            tweet_content = generate_ai_tweet(prompt, message_queue, refine=True)
            time.sleep(3)
        else:
            if not tweets:
                logging.warning("No tweets available in file. Switching to AI mode without refinement.")
                tweet_content = generate_ai_tweet(prompt, message_queue, refine=False)
            else:
                tweet_content = tweets[tweet_index]
                tweet_index = (tweet_index + 1) % len(tweets)
                if message_queue:
                    message_queue.put({"type": "preview", "content": f"Next tweet: {tweet_content}"})
                time.sleep(3)
        
            logging.info(f"Attempting to post tweet: {tweet_content}")
            success, message = post_tweet(tweet_content)
            if message_queue:
                message_queue.put({"type": "posted", "content": message})
        
        sleep_time = max(0, interval - 3)
        time.sleep(sleep_time)

# Streamlit App
def main():
    # Custom CSS for styling
    st.markdown("""
        <style>
        .title { color: #1DA1F2; font-size: 36px; font-weight: bold; }
        .sidebar .sidebar-content { background-color: #f0f2f6; padding: 20px; border-radius: 10px; }
        .stButton>button { background-color: #1DA1F2; color: white; border-radius: 5px; }
        .stButton>button:hover { background-color: #0d8bf2; }
        .preview-box { background-color: #e6f3ff; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
        .posted-box { background-color: #e6ffe6; padding: 10px; border-radius: 5px; }
        .status-running { color: #28a745; font-weight: bold; }
        .status-stopped { color: #dc3545; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    # Header with Twitter-like branding
    st.markdown(
    '<p style="font-size:48px; font-weight:bold;">Twitter Posting Bot</p>', 
    unsafe_allow_html=True
)

    st.write("🚀 Automate your tweets with style and ease!")

    # Initialize session state
    if 'agent_thread' not in st.session_state:
        st.session_state['agent_thread'] = None
    if 'stop_event' not in st.session_state:
        st.session_state['stop_event'] = threading.Event()
    if 'last_tweet' not in st.session_state:
        st.session_state['last_tweet'] = "No tweets posted yet."
    if 'next_tweet' not in st.session_state:
        st.session_state['next_tweet'] = "No tweet queued yet."
    if 'prompt' not in st.session_state:
        st.session_state['prompt'] = None
    if 'message_queue' not in st.session_state:
        st.session_state['message_queue'] = queue.Queue()

    # Sidebar for configuration
    with st.sidebar:
        st.title("⚙️ Control Panel")

        interval = st.number_input(
            "Posting Interval (hours)",
            min_value=0.01,
            max_value=48.0,  # Maximum 24 hours
            value=1.0,      # Default 1 hour
            step=1.0,       # Increment by 0.1 hours (6 minutes)
            help="Set how often tweets are posted (in hours).",
            # format="%.1f"   # Display with 1 decimal place
        ) * 3600  # Convert hours to seconds
        
        use_ai = st.checkbox(
            "Enable AI Tweet Generator",
            value=False,
            help="Toggle to generate tweets with AI instead of using tweets.txt."
        )
        st.sidebar.markdown(
    '<p style="color:red;">Check Above Box to generate responses through AI or else tweets will be fetched from the local storage.</p>', 
    unsafe_allow_html=True
)

        if use_ai:
            st.session_state['prompt'] = st.text_input(
                "AI Prompt (optional)",
                "",
                help="Enter a theme or idea for AI-generated tweets (e.g., 'Tech humor')."
            ) or None
        else:
            st.session_state['prompt'] = None

        # Start/Stop buttons with status
        st.markdown('<div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 10px;">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.write("🚀 **Start**: Begins posting tweets at the set interval.")
            if st.button("Start", key="start"):
                if st.session_state['agent_thread'] is None or not st.session_state['agent_thread'].is_alive():
                    st.session_state['stop_event'].clear()
                    st.session_state['agent_thread'] = threading.Thread(
                        target=twitter_agent,
                        args=(interval, use_ai, st.session_state['stop_event'], st.session_state['prompt'], st.session_state['message_queue']),
                        daemon=True
                    )
                    st.session_state['agent_thread'].start()
                    st.success("Agent started!")
                else:
                    st.warning("Agent is already running!")

        with col2:
            st.write("🛑 **Stop**: Halts the tweet posting process.")
            if st.button("Stop", key="stop"):
                if st.session_state['agent_thread'] is not None and st.session_state['agent_thread'].is_alive():
                    st.session_state['stop_event'].set()
                    st.session_state['agent_thread'].join(timeout=2)
                    if not st.session_state['agent_thread'].is_alive():
                        st.session_state['agent_thread'] = None  # Clear the thread reference
                        st.success("Agent stopped!")
                    else:
                        st.error("Failed to stop agent cleanly. Check logs.")
                else:
                    st.warning("No agent running!")
        st.markdown('</div>', unsafe_allow_html=True)

        # Agent status
        status = "Running" if st.session_state['agent_thread'] and st.session_state['agent_thread'].is_alive() else "Stopped"
        st.markdown(f"**Agent Status:** <span class='status-{'running' if status == 'Running' else 'stopped'}'>{status}</span>", unsafe_allow_html=True)

    # Main content area
    st.subheader("📬 Tweet Queue")
    try:
        while not st.session_state['message_queue'].empty():
            message = st.session_state['message_queue'].get_nowait()
            if message["type"] == "preview":
                st.session_state['next_tweet'] = message["content"]
            elif message["type"] == "posted":
                st.session_state['last_tweet'] = message["content"]
    except queue.Empty:
        pass

    # Tweet preview and posted sections with styling
    st.markdown(f'<div class="preview-box">{st.session_state["next_tweet"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="posted-box">{st.session_state["last_tweet"]}</div>', unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # Logs expander
    with st.expander("📜 View Logs", expanded=False):
        if os.path.exists('twitter_agent.log'):
            with open('twitter_agent.log', 'r') as log_file:
                st.text_area("Log Output", log_file.read(), height=200)
        else:
            st.write("No logs available yet.")

if __name__ == "__main__":
    try:
        api.verify_credentials()
        logging.info("Twitter API authentication successful.")
        if not os.getenv("OPENAI_API_KEY"):
            st.error("OPENAI_API_KEY not found in .env file.")
        else:
            main()
    except tweepy.TweepyException as e:
        logging.error(f"Authentication failed: {e}")
        st.error(f"Failed to authenticate with Twitter: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        st.error(f"An error occurred: {e}")
