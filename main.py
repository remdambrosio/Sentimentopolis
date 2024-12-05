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
    parser = argparse.ArgumentParser(description='analyzes devices to predict site health')
    parser.add_argument('-pu', '--pull', action='store_true', help='pull new data from PRAW')
    args = parser.parse_args()

    if args.pull:
        pull()


def pull():
    """
    Pulls data
    """
    puller = Puller()
    puller.pull_hot_posts('DestinyTheGame')


if __name__ == '__main__':
    main()
