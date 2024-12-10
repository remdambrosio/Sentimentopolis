"""
analyzer.py
Defines class to handle preprocessing and sentiment analysis
"""
import re
import emoji
import json
from textblob import TextBlob


class Analyzer:
    """
    Class to handle interactions with PRAW
    """
    def __init__(self, in_path):
        self.data = self.read_data_json(in_path)
        self.analysis = []
        self.report = []


    # MAIN METHODS =========================


    def comment_sentiment(self):
        """
        Performs sentiment analysis on comments
        """
        analysis = []
        for post in self.data:
            for comment in post['comments']:
                body = self.clean_text(comment['body'])
                analysis.append({
                    'body': body,
                    'score': comment['score'],
                    'sentiment': self.get_sentiment(body),
                })
        self.analysis = analysis
        return


    # HELPER METHODS =======================


    def get_sentiment(self, text):
        """
        Performs sentiment analysis on string
        """
        clean_text = self.clean_text(text)
        polarity = TextBlob(clean_text).correct().sentiment
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


    def write_analysis_json(self, out_path):
        """
        Writes analysis to json
        """
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis, f, indent=4)
        return
