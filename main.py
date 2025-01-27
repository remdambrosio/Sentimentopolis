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
    parser.add_argument('-ps', '--pull_subreddit', type=str, help='subreddit to pull', default='DestinyTheGame')
    parser.add_argument('-pt', '--pull_type', type=str, help='filter type: top/hot/new', default='top')
    parser.add_argument('-pc', '--pull_count', type=int, help='number of posts to pull', default=100)
    parser.add_argument('-pi', '--pull_time', type=str, help='time frame: day/month/year/all', default='year')

    parser.add_argument('-an', '--analyze', action='store_true', help='analyze data from file')
    parser.add_argument('-aa', '--analyze_attribute', type=str, help='analysis attribute: sentiment, nsfwness, saltiness', default='sentiment')
    parser.add_argument('-if', '--input_file', type=str, help='path to input file for analysis', default='data/raw/posts.json')

    parser.add_argument('-re', '--report', action='store_true', help='write report on results')

    args = parser.parse_args()

    if args.pull:
        pull(subreddit=args.pull_subreddit, type=args.pull_type, count=args.pull_count, time=args.pull_time)

    if args.analyze:
        analyze(attribute=args.analyze_attribute, in_file=args.input_file)

    if args.report:
        report()


def pull(subreddit, type, count, time):
    """
    Pulls data
    """
    puller = Puller()
    print('Pulling data...')
    puller.pull_posts(subreddit_name=subreddit, pull_type=type, post_count=count, time_frame=time)
    print('...Data pulled...')
    puller.write_posts_json('data/raw/posts.json')
    print('...Data written to file.')
    return


def analyze(attribute, in_file='data/raw/posts.json'):
    """
    Analyzes data
    """
    print('Analyzing data...')
    analyzer = Analyzer(in_path=in_file, analysis_attribute=attribute, use_gpu=True)
    analyzer.trajectory_analysis(score_threshold=1)
    print('...Analysis gathered...')
    analyzer.write_results_json('data/processed/results.json')
    print('...Analysis written to file.')
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
