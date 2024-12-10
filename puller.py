"""
puller.py
Defines class to handle interactions with PRAW (Python Reddit API Wrapper)
"""
import json
import praw
import config
from textblob import TextBlob


class Puller:
    """
    Class to handle interactions with PRAW
    """
    def __init__(self):
        self.reddit = praw.Reddit(client_id=config.CLIENT_ID,
                                client_secret=config.CLIENT_SECRET,
                                user_agent=config.USER_AGENT)
        self.data = []


    # MAIN METHODS =========================


    def pull_hot_posts(self, subreddit_name, count):
        """
        Adds posts from "hot" feed of input subreddit
        """
        subreddit = self.reddit.subreddit(subreddit_name)
        hot_post_list = subreddit.hot(limit=count)
        expanded_list = self.expand_post_list(hot_post_list)
        self.data = self.data + expanded_list
        return


    # HELPER METHODS =======================


    def expand_post_list(self, post_list):
        """
        Flattens list of PRAW post objects into dict of posts + their comments
        """
        expanded_list = []
        for post in post_list:
            post_data = {                                       # data for post itself
                'id': post.id,
                'title': post.title,
                'selftext': post.selftext,
                'url': post.url,
                'author': str(post.author),
                'created_utc': post.created_utc,
                'score': post.score,
                'comments': []
            }
            post.comments.replace_more(limit=None)              # expand + flatten comment tree
            comments = post.comments.list()
            for comment in comments:
                post_data['comments'].append({
                    'id': comment.id,
                    'author': str(comment.author),
                    'body': comment.body,
                    'created_utc': comment.created_utc,
                    'score': comment.score
                })
            expanded_list.append(post_data)
        return expanded_list


    # I/O METHODS ==========================


    def write_posts_json(self, path):
        """
        Writes data to json
        """
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)
        return
