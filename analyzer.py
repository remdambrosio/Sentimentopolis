"""
analyzer.py
Defines class to handle preprocessing and sentiment analysis
"""
import re
import json
from datetime import datetime

import emoji
from transformers import pipeline


class Analyzer:
    """
    Class to handle interactions with PRAW
    """
    def __init__(self, in_path, use_gpu=True):
        self.data = self.read_data_json(in_path)
        device = 0 if use_gpu else -1
        model_name = 'cardiffnlp/twitter-roberta-base-sentiment'
        self.sentiment_analyzer = pipeline('sentiment-analysis', model=model_name, device=device,
                                           truncation=True, max_length=511)     # only some models require max_length
        self.results = []


    # MAIN METHODS =========================


    def trajectory_analysis(self, score_threshold=1):
        """
        Gets mean comment polarity by day, using only comments with score above threshold
        """
        daily_comments = {}                                 # {date:[comments,on,that,day]}
        length = len(self.data)
        for i, post in enumerate(self.data):                # iterate through all posts + their comments
            for comment in post['comments']:
                if comment['score'] > score_threshold:      # consider popular comments only
                    date = datetime.fromtimestamp(comment['created_utc']).strftime('%Y-%m-%d')
                    comment_text = self.clean_text(comment['body'])
                    if date not in daily_comments:          # add each comment to appropriate day
                        daily_comments[date] = [comment_text]
                    else:
                        daily_comments[date].append(comment_text)
            print(f'...Collected comments from post {i+1} of {length}...')

        sorted_days = sorted(daily_comments.keys(), key=lambda x: datetime.strptime(x, '%Y-%m-%d'))

        trajectory = []
        length = len(sorted_days)
        for i, date in enumerate(sorted_days):              # batch process polarity for each day
            polarity = self.get_sentiment(daily_comments[date])
            trajectory.append((date, polarity))
            print(f'...Analyzed date {i+1} of {length}...')

        self.results += trajectory
        return


    # HELPER METHODS =======================


    def get_sentiment(self, text_batch):
        """
        Prepares text and gets sentiment (compartmentalized in case I want to swap later)
        """
        sentiment = self.huggingface_polarity(text_batch)
        return sentiment
    

    def huggingface_polarity(self, text_batch):
        """
        Gets average polarity of a list of strings using Hugging Face
        """
        label_to_polarity = {"LABEL_0": -1, "LABEL_1": 0, "LABEL_2": 1}
        string_sentiments = self.sentiment_analyzer(text_batch)
        total = 0
        for entry in string_sentiments:
            polarity = label_to_polarity[entry['label']]
            total += polarity
        avg_polarity = total / len(string_sentiments)
        return avg_polarity


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
