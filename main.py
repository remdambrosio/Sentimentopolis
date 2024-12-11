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
    puller.pull_posts('DestinyTheGame', pull_type='top', post_count=1000, time_frame='month')
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
    analyzer.trajectory_analysis()
    print('...Sentiment gathered...')
    analyzer.write_results_json('data/output/results.json')
    print('...Results written to file.')
    return


if __name__ == '__main__':
    main()
