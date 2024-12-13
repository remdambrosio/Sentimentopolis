"""
reporter.py
Defines class to handle reporting and visualization
"""
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Reporter:
    """
    Class to handle reporting and visualization
    """
    def __init__(self, in_path):
        self.results = self.read_results_json(in_path)


    # MAIN METHODS =========================


    def visualize_trajectory(self):
        """
        Generates report on trajectory results
        """
        start_date = self.results[0][0]
        df = pd.DataFrame(self.results, columns=['Date', 'Polarity'])
        df['Date'] = pd.to_datetime(df['Date'])
        df['DateNumeric'] = (df['Date'] - df['Date'].min()).dt.days

        plt.figure(figsize=(10, 6))
        sns.regplot(data=df, x='DateNumeric', y='Polarity', scatter=True, fit_reg=True,
                    marker='o', color='blue', line_kws={'color': 'red'}, ci=None)
        plt.title('Popular Comment Polarity', fontsize=16)
        plt.xlabel(f'Days from {start_date}', fontsize=12)
        plt.ylabel('Polarity', fontsize=12)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        return


    # I/O METHODS ==========================


    def read_results_json(self, in_path):
        """
        Reads json to results
        """
        with open(in_path, 'r', encoding='utf-8') as file:
            results = json.load(file)
        return results
