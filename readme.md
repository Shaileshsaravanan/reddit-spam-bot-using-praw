# reddit-spam-bot-using-praw

A Reddit bot that detects and flags spam content based on customizable search terms using the PRAW (Python Reddit API Wrapper) library.

## Features

- **Customizable Search Terms**: Define your own list of keywords to search for spammy content across all subreddits.
- **Spam Detection**: Analyzes users' submissions and calculates a "spam score" to determine if they are likely spammers.
- **Automated Replies**: The bot replies to identified spammy submissions, alerting the community about potential spam.
- **Flexible Configuration**: Easily toggle debug mode, adjust spam thresholds, and modify search terms.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/shaileshsaravanan/reddit-spam-bot-using-praw.git
    cd reddit-spam-bot-using-praw
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up your environment variables**:

    Create a `.env` file in the root directory and add your Reddit API credentials:

    ```plaintext
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    PASSWORD=your_password
    USER_AGENT=your_user_agent
    USERNAME=your_username
    ```

5. **Create the `spam_words.txt` file**:

    This file should contain a list of words/phrases to be used for identifying spam, one per line:

    ```plaintext
    udemy
    coupon
    free course
    discount
    limited offer
    ```

6. **Create the `posted_urls.txt` file**:

    This file keeps track of the URLs the bot has already replied to. You can create an empty file or add URLs that should be ignored:

    ```plaintext
    https://reddit.com/r/example_post_1
    https://reddit.com/r/example_post_2
    ```

## Usage

1. **Run the bot**:
    ```bash
    python main.py
    ```

    The bot will start searching for spam content based on the search terms defined in the `main.py` file.

2. **Adjust the search terms**:

    You can modify the `search_terms` list in the `main.py` file to include any keywords you want the bot to search for.

3. **Enable/Disable Debug Mode**:

    If `DEBUG_MODE` is set to `True`, the bot will not post replies to Reddit but will print what it would have posted.

## Contributing

Feel free to submit issues, fork the repository, and send pull requests. Contributions are welcome!