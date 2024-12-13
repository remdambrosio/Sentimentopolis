"""
main.py
Main function for Sentimentopolis
"""
import argparse
from puller import Puller
from analyzer import Analyzer
from reporter import Reporter


def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(description='Does PRAW stuff')
    parser.add_argument('-pu', '--pull', action='store_true', help='pull new data from PRAW')
    parser.add_argument('-an', '--analyze', action='store_true', help='analyze data from file')
    parser.add_argument('-re', '--report', action='store_true', help='write report on results')
    args = parser.parse_args()

    if args.pull:
        pull()

    if args.analyze:
        analyze()

    if args.report:
        report()


def pull():
    """
    Pulls data
    """
    puller = Puller()
    print('Pulling data...')
    puller.pull_posts('DestinyTheGame', pull_type='top', post_count=10, time_frame='month')
    print('...Data pulled...')
    puller.write_posts_json('data/raw/posts.json')
    print('...Data written to file.')
    return


def analyze():
    """
    Analyzes data
    """
    print('Analyzing data...')
    analyzer = Analyzer(in_path='data/raw/posts.json', use_gpu=True)
    analyzer.trajectory_analysis()
    print('...Sentiment gathered...')
    analyzer.write_results_json('data/processed/results.json')
    print('...Results written to file.')
    return


def report():
    """
    Reports results
    """
    print('Reporting results...')
    reporter = Reporter(in_path='data/processed/results.json')
    reporter.visualize_trajectory()
    print('...Results reported.')
    return

if __name__ == '__main__':
    main()
