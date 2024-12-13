"""
puller.py
Defines class to handle interactions with PRAW (Python Reddit API Wrapper)
"""
import json
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
        Flattens list of PRAW post objects into list of posts + their comments
        """
        post_list = list(posts)
        expanded_list = []
        length = len(post_list)
        for i, post in enumerate(post_list):
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

            post.comments.replace_more(limit=0)                 # trim "load more comments"
            comments = post.comments.list()                     # data for comments
            for comment in comments:
                post_data['comments'].append({
                    'id': comment.id,
                    'author': str(comment.author),
                    'body': comment.body,
                    'created_utc': comment.created_utc,
                    'score': comment.score
                })

            expanded_list.append(post_data)
            print(f'...Pulled comments from post {i+1} of {length}...')

        return expanded_list


    # I/O METHODS ==========================


    def write_posts_json(self, path):
        """
        Writes data to json
        """
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)
        return
