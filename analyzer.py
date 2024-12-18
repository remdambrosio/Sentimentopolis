"""
analyzer.py
Defines class to handle preprocessing and sentiment analysis
"""
import json
from datetime import datetime
from transformers import pipeline


class Analyzer:
    """
    Class to handle interactions with PRAW
    """
    def __init__(self, in_path, analysis_attribute, use_gpu):
        self.data = self.read_data_json(in_path)
        self.analysis_attribute = analysis_attribute
        device = 0 if use_gpu else -1
        if analysis_attribute == 'sentiment':
            model_name = 'cardiffnlp/twitter-roberta-base-sentiment'
        elif analysis_attribute == 'nsfwness':
            model_name = 'eliasalbouzidi/distilbert-nsfw-text-classifier'
        self.sentiment_analyzer = pipeline('sentiment-analysis', model=model_name, device=device, truncation=True, max_length=511)

        self.results = []


    # MAIN METHODS =========================


    def trajectory_analysis(self, score_threshold):
        """
        Analyzes comments by day, using only comments with score (upvotes - downvotes) above threshold
        """
        daily_comments = {}                                 # {date:[comments,on,that,day]}
        length = len(self.data)
        for i, post in enumerate(self.data):                # iterate through all posts + their comments
            for comment in post['comments']:
                if comment['score'] > score_threshold:      # consider popular comments only
                    date = datetime.fromtimestamp(comment['created_utc']).strftime('%Y-%m-%d')
                    if date not in daily_comments:          # add each comment to appropriate day
                        daily_comments[date] = [comment['body']]
                    else:
                        daily_comments[date].append(comment['body'])
            print(f'...Collected comments from post {i+1} of {length}...')

        sorted_days = sorted(daily_comments.keys(), key=lambda x: datetime.strptime(x, '%Y-%m-%d'))

        trajectory = []
        length = len(sorted_days)
        for i, date in enumerate(sorted_days):              # batch process sentiment for each day
            if len(daily_comments[date]) > 5:
                sentiment = self.get_analysis(text_batch=daily_comments[date])
                trajectory.append((date, sentiment))
                print(f'...Analyzed date {i+1} of {length}...')
            else:
                print(f'...Low comment count on date {i+1} of {length}...')

        self.results += trajectory
        return


    # HELPER METHODS =======================


    def get_analysis(self, text_batch):
        """
        Analyzes text batch based on chosen analysis attribute
        """
        if self.analysis_attribute == 'sentiment':
            analysis_result = self.transformer_sentiment(text_batch)
        elif self.analysis_attribute == 'nsfwness':
            analysis_result = self.transformer_nsfwness(text_batch)
        return analysis_result
    

    def transformer_sentiment(self, text_batch):
        """
        Gets average sentiment of a list of strings
        """
        label_to_sentiment = {"LABEL_0": -1, "LABEL_1": 0, "LABEL_2": 1}
        string_sentiments = self.sentiment_analyzer(text_batch)
        total = 0
        for entry in string_sentiments:
            sentiment = label_to_sentiment[entry['label']]
            total += sentiment
        avg_sentiment = total / len(string_sentiments)
        return avg_sentiment
    

    def transformer_nsfwness(self, text_batch):
        """
        Gets average nsfwness of a list of strings
        """
        label_to_nsfwness = {"safe": 0, "nsfw": 1}
        string_sentiments = self.sentiment_analyzer(text_batch)
        total = 0
        for entry in string_sentiments:
            nsfwness = label_to_nsfwness[entry['label']]
            total += nsfwness
        avg_nsfwness = total / len(string_sentiments)
        return avg_nsfwness


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
        results_dict = {
            'analysis_type':self.analysis_attribute,
            'dates':self.results
        }
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, indent=4)
        return
