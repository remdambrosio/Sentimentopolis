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
    comments = puller.pull_hot_comments('DestinyTheGame', 1)
    for comment in comments:
        print(f"===== Score: {comment['score']}, Sentiment: {comment['polarity']:.2f} =====")
        print(comment['body'])


if __name__ == '__main__':
    main()
