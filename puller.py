"""
puller.py
Defines class to handle interactions with PRAW (Python Reddit API Wrapper)
"""
import json
import praw
import config
import emoji
import re


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


    def pull_posts(self, subreddit_name, pull_type='new', post_count=1000, time_frame='all'):
        """
        Adds posts from a subreddit to data
        """
        subreddit = self.reddit.subreddit(subreddit_name)

        if pull_type == 'new':
            posts = subreddit.new(limit=post_count)
        elif pull_type == 'top':
            posts = subreddit.top(limit=post_count, time_filter=time_frame)
        elif pull_type == 'hot':
            posts = subreddit.hot(limit=post_count, time_filter=time_frame)
        print(f'...Identified {post_count} posts via PRAW...')

        expanded_list = self.expand_post_list(posts)

        self.data = self.data + expanded_list
        return


    # HELPER METHODS =======================


    def expand_post_list(self, posts):
        """
        Flattens collection of PRAW post objects into list of posts + their comments
        """
        post_list = list(posts)
        expanded_list = []
        length = len(post_list)
        for i, post in enumerate(post_list):
            post_data = {                                       # data for post itself
                'id': post.id,
                'title': self.clean_text(post.title),
                'selftext': self.clean_text(post.selftext),
                'url': post.url,
                'author': str(post.author),
                'created_utc': post.created_utc,
                'score': post.score,
                'comments': []
            }

            post.comments.replace_more(limit=0)                 # trim "load more comments"
            comments = post.comments.list()                     # data for comments
            for comment in comments:
                post_data['comments'].append({
                    'id': comment.id,
                    'author': str(comment.author),
                    'body': self.clean_text(comment.body),
                    'created_utc': comment.created_utc,
                    'score': comment.score
                })

            expanded_list.append(post_data)
            print(f'...Pulled comments from post {i+1} of {length}...')

        return expanded_list


    def clean_text(self, text):
        """
        Cleans text and replaces common flamboyant characters with their common equivalent
        """
        translations = str.maketrans({
            '\u2018': "'",
            '\u2019': "'",
            '\u201C': '"',
            '\u201D': '"',
            '\u2010': '-',
            '\u2011': '-',
            '\u2012': '-',
            '\u2013': '-',
            '\u2014': '-',
            '\u2026': '...',
            '\u00A0': ' ',
            '\u2009': ' ',
            '\u200A': ' ',
            '\u200B': '',
            '\u00B7': '.',
            '\u2022': '*',
            '\u201A': ',',
            '\u2039': '<',
            '\u203A': '>',
        })
        text = text.translate(translations)                     # normalize unicode
        text = emoji.demojize(text)                             # emojis to words
        text = re.sub(r'http[s]?://\S+', '', text)              # strip urls
        text = re.sub(r'/u/\w+|u/\w+', '', text)                # strip username mentions
        text = re.sub(r'<[^>]+>', '', text)                     # strip html tags
        text = re.sub(r'[^a-zA-Z0-9\s!?\'.,#@%$&]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()                # compress whitespace
        text = text.lower()                                     # case
        return text


    # I/O METHODS ==========================


    def write_posts_json(self, path):
        """
        Writes data to json
        """
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)
        return
