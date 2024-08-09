import praw
import re
import os
import random
import time
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    password=os.getenv("PASSWORD"),
    user_agent=os.getenv("USER_AGENT"),
    username=os.getenv("USERNAME")
)

DEBUG_MODE = False
DEBUG_POSTED = []
SPAM_THRESHOLD = 0.5
POSTED_URLS_FILE = "posted_urls.txt"
SPAM_WORDS_FILE = "spam_words.txt"

def load_spam_words():
    spam_words = []
    try:
        with open(SPAM_WORDS_FILE, "r") as f:
            spam_words = [re.compile(line.strip(), re.IGNORECASE) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {SPAM_WORDS_FILE} not found.")
    return spam_words

def find_spammy_authors(search_terms):
    authors = set()
    try:
        for term in search_terms:
            print(f"Searching for term: {term}")
            for submission in reddit.subreddit("all").search(term, sort="new", limit=20):
                print(f"Checking submission: {submission.title} by {submission.author}")
                authors.add(submission.author)
    except Exception as e:
        print(f"Error finding spammy authors: {e}")
    return authors

def analyze_user_submissions(author, spam_patterns):
    spammy_submissions = []
    try:
        submissions = list(reddit.redditor(str(author)).submissions.new(limit=None))
        if not submissions:
            return 0.0, 0, spammy_submissions

        spam_count = 0
        for submission in submissions:
            if any(pattern.search(submission.title) for pattern in spam_patterns):
                spam_count += 1
                spammy_submissions.append((submission.id, submission.title, author))

        spam_score = spam_count / len(submissions)
        return spam_score, len(submissions), spammy_submissions

    except Exception as e:
        print(f"Error analyzing submissions for {author}: {e}")
        return 0.0, 0, spammy_submissions

def load_posted_urls():
    if os.path.exists(POSTED_URLS_FILE):
        with open(POSTED_URLS_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_posted_url(url):
    with open(POSTED_URLS_FILE, "a") as f:
        f.write(url + "\n")

def post_reply(submission, message, posted_urls):
    link = f"https://reddit.com{submission.permalink}"
    if link not in posted_urls:
        if DEBUG_MODE:
            if link in DEBUG_POSTED:
                return
            print(f"DEBUG: Would have posted reply to {link}")
            DEBUG_POSTED.append(link)
        else:
            try:
                submission.reply(message)
                print(f"Posted reply to {link}")
                save_posted_url(link)
                time.sleep(12 * 60)
            except Exception as e:
                print(f"Error posting reply: {e}")
                time.sleep(12 * 60)

def main(search_terms):
    spam_patterns = load_spam_words()
    if not spam_patterns:
        return

    posted_urls = load_posted_urls()

    while True:
        spammy_authors = find_spammy_authors(search_terms)

        for author in spammy_authors:
            spam_score, submission_count, spammy_submissions = analyze_user_submissions(author, spam_patterns)

            if spam_score >= SPAM_THRESHOLD and submission_count > 1:
                for spam_id, spam_title, spam_author in spammy_submissions:
                    submission = reddit.submission(id=spam_id)
                    if time.time() - submission.created_utc <= 86400:
                        message = (f"*Beep boop*\n\nI am a bot that sniffs out spammers, "
                                   f"and this smells like spam.\n\n"
                                   f"At least {round(spam_score * 100, 2)}% of the {submission_count} submissions "
                                   f"from /u/{spam_author} appear to be for spam content.\n\n"
                                   f"Don't let spam take over Reddit! Throw it out!\n\n*Bee bop*")
                        post_reply(submission, message, posted_urls)

        print("Sleeping for a bit before the next search...")
        time.sleep(60 * 10)

if __name__ == "__main__":
    search_terms = ["udemy", "coupon", "free course", "discount", "limited offer"]
    main(search_terms)