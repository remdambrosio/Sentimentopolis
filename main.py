"""
main.py
Main function for Sentimentopolis
"""
import argparse
from puller import Puller
from analyzer import Analyzer


def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(description='Does PRAW stuff')
    parser.add_argument('-pu', '--pull', action='store_true', help='pull new data from PRAW')
    parser.add_argument('-an', '--analyze', action='store_true', help='analyzes data from file')
    args = parser.parse_args()

    if args.pull:
        pull()

    if args.analyze:
        analyze()


def pull():
    """
    Pulls data
    """
    puller = Puller()
    print('Pulling data...')
    puller.pull_hot_posts('DestinyTheGame', 3)
    print('...Data pulled...')
    puller.write_posts_json('data/input/posts.json')
    print('...Data written to file.')
    return


def analyze():
    """
    Analyzes data
    """
    print('Analyzing data...')
    analyzer = Analyzer('data/input/posts.json')
    analyzer.comment_sentiment()
    print('...Data analyzed...')
    analyzer.write_analysis_json('data/output/analysis.json')
    print('...Analysis written to file.')
    return


if __name__ == '__main__':
    main()
