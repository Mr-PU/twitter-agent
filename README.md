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

- Python 3.7+
- Twitter Developer Account with API credentials
- OpenAI API key

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/twitter-posting-bot.git
cd twitter-posting-bot
