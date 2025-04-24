import json
import pandas as pd
import os

class createDataFrame:
    def __init__(self):
        self.data = None

    def load_json(self, file_path):
        with open(file_path, 'r') as f:
            self.data = json.load(f)

    def load_all_json(self, folder_path='./data/'):
        self.data = []
        for file in os.listdir(folder_path):
            if file.endswith('.json'):
                with open(os.path.join(folder_path, file), 'r') as f:
                    self.data.append(json.load(f))

    def create_dataframe_from_file(self, data):
        questionnaire_df = pd.DataFrame({
            'user_id': data['userData']['id'],
            'name': data['userData']['name'],
            'indexes': data['questionaireData']['indexes'],
            'answers': data['questionaireData']['answers'],
            'subscales': data['questionaireData']['subscales'],
            'source': 'questionnaire'
        })

        game_df = pd.DataFrame({
            'user_id': data['userData']['id'],
            'name': data['userData']['name'],
            'difficulty': data['gameData']['difficulties'],
            'time': data['gameData']['times'],
            'result': data['gameData']['results'],
            'source': 'game'
        })

        test_df = pd.DataFrame({
            'user_id': data['userData']['id'],
            'name': data['userData']['name'],
            'difficulty': data['testData']['difficulty'],
            'time': data['testData']['times'],
            'answers': data['testData']['answers'],
            'source': 'test'
        })

        # Spalten anpassen, damit mergebar
        game_df = game_df.rename(columns={'result': 'answers'})
        game_df['indexes'] = range(1, len(game_df) + 1)
        game_df['subscales'] = None # Platzhalter für einheitliche Struktur

        test_df['indexes'] = range(1, len(test_df) + 1)
        test_df['subscales'] = None  # Platzhalter für einheitliche Struktur

        # Vereinheitlichte Reihenfolge der Spalten
        cols = ['user_id', 'name', 'indexes', 'answers', 'subscales', 'difficulty', 'time', 'source']
        all_data = pd.concat([questionnaire_df, game_df[cols], test_df[cols]], ignore_index=True)

        return all_data
    
    
    def create_dataframe(self):
        dataframes = []
        if self.data is None:
            raise ValueError("load_json aufrufen. Keine Daten eingelesen")
        
        if isinstance(self.data, list):
            for d in self.data:
                dataframes.append(self.create_dataframe_from_file(d))
            return dataframes
        
        dataframes.append(self.create_dataframe_from_file(self.data))
        return dataframes
            
    def save_dataframe(self, dflist, folder_path='./dataframes/'):
        for i in range(len(dflist)):
            if not isinstance(dflist[i], pd.DataFrame):
                raise ValueError("Die Liste enthält kein DataFrame-Objekt.")
            dflist[i].to_csv(folder_path + str(i) + ".csv", index=False, encoding='utf-8')
            print(f"DataFrame {i} gespeichert unter {folder_path}")

    