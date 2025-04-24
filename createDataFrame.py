import json
import pandas as pd

class createDataFrame:
    def __init__(self):
        self.data = None

    def load_json(self, file_path):
        with open(file_path, 'r') as f:
            self.data = json.load(f)

    def create_dataframe(self):
        if self.data is None:
            raise ValueError("load_json aufrifen. keine daten eingelesen")
        d = self.data

        questionnaire_df = pd.DataFrame({
            'user_id': d['userData']['id'],
            'name': d['userData']['name'],
            'index': d['questionaireData']['indexes'],
            'answer': d['questionaireData']['answers'],
            'subscale': d['questionaireData']['subscales'],
            'source': 'questionnaire'
        })

        game_df = pd.DataFrame({
            'user_id': d['userData']['id'],
            'name': d['userData']['name'],
            'difficulty': d['gameData']['difficulties'],
            'time': d['gameData']['times'],
            'result': d['gameData']['results'],
            'source': 'game'
        })

        test_df = pd.DataFrame({
            'user_id': d['userData']['id'],
            'name': d['userData']['name'],
            'difficulty': d['testData']['difficulty'],
            'time': d['testData']['times'],
            'answer': d['testData']['answers'],
            'source': 'test'
        })

        # Spalten anpassen, damit mergebar
        game_df = game_df.rename(columns={'result': 'answer'})
        game_df['index'] = range(1, len(game_df) + 1)

        test_df['index'] = range(1, len(test_df) + 1)
        test_df['subscale'] = None  # Platzhalter für einheitliche Struktur

        # Vereinheitlichte Reihenfolge der Spalten
        cols = ['user_id', 'name', 'index', 'answer', 'subscale', 'difficulty', 'time', 'source']
        all_data = pd.concat([questionnaire_df, game_df[cols], test_df[cols]], ignore_index=True)

        return all_data
