"""
puller.py
Defines class to handle interactions with PRAW (Python Reddit API Wrapper)
"""

import praw
import config

class Puller:
    """
    Class to handle interactions with PRAW
    """
    def __init__(self):
        self.reddit = praw.Reddit(client_id=config.CLIENT_ID,
                                client_secret=config.CLIENT_SECRET,
                                user_agent=config.USER_AGENT)


    def pull_hot_posts(self, subreddit, num):
        """
        Pulls and displays top posts on "hot" feed of input subreddit
        """
        hot_posts = self.reddit.subreddit(subreddit).hot(limit=num)
        return hot_posts
