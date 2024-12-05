"""
puller.py
Defines class to handle interactions with PRAW (Python Reddit API Wrapper)
"""

import praw
import config
import pandas as pd
import re

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
        comments_list = []
        for post in posts:
            post.comments.replace_more(limit=None)                      # all comment trees expanded + flattened
            for comment in post.comments.list():
                body = self.clean_body(comment.body)
                comments_list.append({
                    'body': body,
                    'score': comment.score
                })
        comments_df = pd.DataFrame(comments_list)
        return comments_df


    def clean_body(self, body):
        """
        Cleans unwanted characters from comment body
        """
        body = re.sub(r'@[A-Za-z0-9]+', '', body)                   # remove user mentions
        body = re.sub(r'https?:\/\/\S+', '', body)                  # remove hyperlinks
        emoji_pattern = re.compile("["
                                    "\U0001F600-\U0001F64F"
                                    "\U0001F300-\U0001F5FF"
                                    "\U0001F680-\U0001F6FF"
                                    "\U0001F700-\U0001F77F"
                                    "\U0001F780-\U0001F7FF"
                                    "\U0001F800-\U0001F8FF"
                                    "\U0001F900-\U0001F9FF"
                                    "\U0001FA00-\U0001FA6F"
                                    "\U0001FA70-\U0001FAFF"
                                    "\U00002702-\U000027B0"
                                    "\U000024C2-\U0001F251"
                                    "]+", flags=re.UNICODE)
        body = re.sub(emoji_pattern, '', body)
        return body
