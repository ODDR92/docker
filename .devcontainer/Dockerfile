# Start from the Python 3.11 image
FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Update the repository sources list
RUN apt-get update -y

# Install wget, prerequisites for Google Chrome, and Python packages
RUN apt-get install -y wget gdebi-core

# Download Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Install Google Chrome
RUN gdebi -n google-chrome-stable_current_amd64.deb

# Remove the .deb file
RUN rm google-chrome-stable_current_amd64.deb

# Install Python packages
RUN pip install requests webdriver_manager beautifulsoup4 pandas selenium nltk

# Install the OpenAI Python client
RUN pip install openai

# Set the OpenAI API key as an environment variable
ENV OPENAI_API_KEY=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