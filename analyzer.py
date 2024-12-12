"""
analyzer.py
Defines class to handle preprocessing and sentiment analysis
"""
import re
import json
from datetime import datetime

import emoji
from textblob import TextBlob


class Analyzer:
    """
    Class to handle interactions with PRAW
    """
    def __init__(self, in_path):
        self.data = self.read_data_json(in_path)
        self.results = []


    # MAIN METHODS =========================


    def sentiment_analysis(self, score_threshold=1):
        """
        Gets basic info and polarity for popular comments
        """
        results = []
        length = len(self.data)
        for i, post in enumerate(self.data):
            for comment in post['comments']:
                score = comment['score']
                if score > score_threshold:
                    body = comment['body']
                    created_utc = comment['created_utc']
                    sentiment = self.get_sentiment(body)
                    results.append({
                        'body': body,
                        'score': score,
                        'created_utc': created_utc,
                        'sentiment': sentiment,
                    })
            print(f'...Analyzed post {i+1} of {length}...')
        self.results = results
        return


    def trajectory_analysis(self, score_threshold=1):
        """
        Gets mean popular comment polarity by day
        """
        trajectory = []
        daily_sentiment = {}
        length = len(self.data)
        for i, post in enumerate(self.data):                # get polarity of all popular comments
            for comment in post['comments']:
                if comment['score'] > score_threshold:
                    date = datetime.fromtimestamp(comment['created_utc']).strftime('%Y-%m-%d')
                    comment_sentiment = self.get_sentiment(comment['body'])
                    if date not in daily_sentiment:         # aggregate by day
                        daily_sentiment[date] = {
                            'total': comment_sentiment,
                            'count': 1
                        }
                    else:
                        daily_sentiment[date]['total'] += comment_sentiment
                        daily_sentiment[date]['count'] += 1
            print(f'...Analyzed post {i+1} of {length}...')

        sorted_days = sorted(daily_sentiment.keys(), key=lambda x: datetime.strptime(x, '%Y-%m-%d'))

        for date in sorted_days:                            # mean polarity for each day
            total = daily_sentiment[date]['total']
            count = daily_sentiment[date]['count']
            mean = total / count
            trajectory.append((date, mean))

        self.results = trajectory
        return


    # HELPER METHODS =======================


    def get_sentiment(self, text):
        """
        Prepares text and gets sentiment
        """
        text = self.clean_text(text)
        sentiment = self.textblob_polarity(text)
        return sentiment


    def textblob_polarity(self, text):
        """
        Gets string polarity using TextBlob
        """
        polarity = TextBlob(text).correct().sentiment.polarity
        return polarity


    def clean_text(self, text):
        """
        Cleans comment text
        """
        text = emoji.demojize(text)                             # emojis to words
        text = re.sub(r'http[s]?://\S+', '', text)              # urls
        text = re.sub(r'/u/\w+|u/\w+', '', text)                # username mentions
        text = re.sub(r'<[^>]+>', '', text)                     # html tags
        text = re.sub(r'[^a-zA-Z0-9\s!?\'.,]', ' ', text)       # special characters
        text = re.sub(r'\s+', ' ', text).strip()                # whitespace
        text = text.lower()                                     # case
        return text


    # I/O METHODS ==========================


    def read_data_json(self, in_path):
        """
        Reads json to data
        """
        with open(in_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data


    def write_results_json(self, out_path):
        """
        Writes sentiment analysis results to json
        """
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=4)
        return
