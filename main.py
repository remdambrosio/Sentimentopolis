"""
main.py
Main function for Sentimentopolis
"""

import argparse
from puller import Puller

def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(description='Does PRAW stuff')
    parser.add_argument('-pu', '--pull', action='store_true', help='pull new data from PRAW')
    args = parser.parse_args()

    if args.pull:
        pull()


def pull():
    """
    Pulls data
    """
    puller = Puller()
    hot_posts = puller.pull_hot_posts('DestinyTheGame', 10)
    for idx, post in enumerate(hot_posts):
        print(f"{idx+1}: {post.title}")


if __name__ == '__main__':
    main()
