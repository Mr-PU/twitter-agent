# Twitter Posting Bot

## Overview

Twitter Posting Bot is a Streamlit-based application that automates the process of posting tweets to your Twitter account at scheduled intervals. The bot offers dual functionality:

1. **Pre-written Tweets**: Post tweets from a pre-defined text file
2. **AI-Generated Tweets**: Generate tweets using CrewAI agents powered by OpenAI's GPT models

This application is perfect for social media managers, content creators, or anyone looking to maintain a consistent Twitter presence without manual intervention.

## Features

- 🕒 **Scheduled Posting**: Set custom time intervals for automated posting
- 🤖 **AI Tweet Generation**: Use OpenAI's GPT models to create engaging tweets
- ✏️ **Collaborative AI Process**: Two-agent system (writer + editor) for higher quality tweets
- 🔄 **Tweet Preview**: See upcoming tweets before they're posted
- 📝 **Custom Prompts**: Guide AI tweet generation with specific themes or topics
- 📊 **Live Status Updates**: Monitor bot activity with real-time status indicators
- 📜 **Logging**: Keep track of all bot activities with detailed logs
- 🌐 **User-Friendly Interface**: Easy-to-use Streamlit web interface

## Architecture

The application uses a combination of technologies:

- **Streamlit**: For the web interface
- **Tweepy**: For Twitter API interaction
- **CrewAI**: For agent-based AI tweet generation and refinement
- **OpenAI GPT**: For AI content generation
- **Threading**: For background task management

## Installation

### Prerequisites

- Python 3.10+
- Twitter Developer Account with API credentials
- OpenAI API key

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/twitter-posting-bot.git
cd twitter-posting-bot
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If the `requirements.txt` file is not included, create one with the following content:

```
streamlit
tweepy
crewai
openai
python-dotenv
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# Twitter API Credentials
API_KEY=your_twitter_api_key
API_SECRET=your_twitter_api_secret
ACCESS_TOKEN=your_twitter_access_token
ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key
```

### Step 5: Create a Tweets File (Optional)

If you plan to use pre-written tweets, create a `tweets.txt` file in the root directory with one tweet per line:

```
This is my first automated tweet! #TwitterBot
Excited to share more content with you all soon!
Check out my latest project: https://github.com/Mr-PU
```

## Usage

### Starting the Application

```bash
streamlit run app.py
```

This will start the Streamlit server and open the application in your default web browser.

### Using the Interface

1. **Configure Settings**:
   - Set the posting interval in hours (minimum 0.01 hours ≈ 36 seconds)
   - Choose between AI-generated or pre-written tweets
   - If using AI, optionally provide a prompt to guide tweet generation

2. **Start the Bot**:
   - Click the "Start" button to begin the automated posting process
   - The bot will run in the background and post tweets at the specified interval

3. **Monitor Activity**:
   - View the next tweet that will be posted
   - See the status of recently posted tweets
   - Check the agent status (Running/Stopped)

4. **Stop the Bot**:
   - Click the "Stop" button to halt the posting process

### Viewing Logs

The application maintains a detailed log file (`twitter_agent.log`) which can be viewed directly in the application by expanding the "View Logs" section at the bottom of the interface.

## Advanced Configuration

### CrewAI Agents

The application uses two CrewAI agents:

1. **Tweet Writer**: Generates initial tweet drafts
2. **Tweet Editor**: Refines and optimizes the drafts for clarity and engagement

You can modify the agent characteristics and prompts in the code to better suit your needs.

### Twitter API Rate Limits

Be aware of Twitter API rate limits. The application is designed to post at reasonable intervals, but setting very short intervals might exceed your API quota, especially for free developer accounts.

## Troubleshooting

### Common Issues

1. **Authentication Failed**: 
   - Ensure your Twitter API credentials are correct
   - Check that your Twitter Developer App has read/write permissions

2. **OpenAI API Key Invalid**:
   - Verify your OpenAI API key is correct
   - Check that your OpenAI account has sufficient credits

3. **Tweet Posting Failed**:
   - Tweets exceeding 280 characters won't be posted
   - Duplicate tweets might be rejected by Twitter

### Checking Logs

For detailed error information, check:
- The in-app log viewer
- The `twitter_agent.log` file in your project directory

## License

[Include your license information here]

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web interface framework
- [Tweepy](https://www.tweepy.org/) for Twitter API integration
- [CrewAI](https://www.crewai.io/) for agent-based workflow
- [OpenAI](https://openai.com/) for AI language models

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
