"""
puller.py
Defines class to handle interactions with PRAW (Python Reddit API Wrapper)
"""
import praw
import config
import pandas as pd
import re
import emoji
from textblob import TextBlob


class Puller:
    """
    Class to handle interactions with PRAW
    """
    def __init__(self):
        self.reddit = praw.Reddit(client_id=config.CLIENT_ID,
                                client_secret=config.CLIENT_SECRET,
                                user_agent=config.USER_AGENT)


    def pull_hot_comments(self, subreddit, num):
        """
        Pulls comments from top num posts on "hot" feed of input subreddit
        """
        hot_posts = self.reddit.subreddit(subreddit).hot(limit=num)
        hot_comments = self.get_comments(hot_posts)
        return hot_comments


    def get_comments(self, posts):
        """
        Pulls comments from input posts
        """
        comments = []
        for post in posts:
            post.comments.replace_more(limit=None)              # expanded + flattened comment trees
            for comment in post.comments.list():
                body = self.clean_text(comment.body)
                comments.append({
                    'body': body,
                    'score': comment.score,
                    'polarity': TextBlob(body).correct().sentiment.polarity,
                })
        return comments


    def clean_text(self, text):
        """
        Cleans unwanted data from comment text
        """
        text = emoji.demojize(text)                             # emojis to words
        text = re.sub(r'http[s]?://\S+', '', text)              # urls
        text = re.sub(r'/u/\w+|u/\w+', '', text)                # username mentions
        text = re.sub(r'<[^>]+>', '', text)                     # html tags
        text = re.sub(r'[^a-zA-Z0-9\s!?\'.,]', ' ', text)       # special characters
        text = re.sub(r'\s+', ' ', text).strip()                # whitespace
        text = text.lower()                                     # case
        return text
