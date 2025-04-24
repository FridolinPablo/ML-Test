import pandas as pd
from buildVektor import VectorBuilder
from calcVektordif import DistanceCalculator
import numpy as np

class UserProfileBuilder:
    def __init__(self, df):
        self.df = df

    def normalize_likert(self, x):
        return (x - 1) / 5

    def safe_mean(self, x):
        return x.mean() if not x.empty else 0

    def safe_std(self, x):
        return x.std() if not x.empty else 0

    def build_profiles(self):
        profiles = []
        for user_id, group in self.df.groupby("user_id"):
            name = group["name"].iloc[0]

            # Spielverhalten
            game = group[group["source"] == "game"].copy()
            game["difficulty"] = game["difficulty"].astype(float) / 2
            game["time"] = game["time"].astype(float)

            game_features = {
                "game_difficulty_mean": self.safe_mean(game["difficulty"]),
                "game_difficulty_std": self.safe_std(game["difficulty"]),
                "game_time_mean": self.safe_mean(game["time"]),
                "game_time_std": self.safe_std(game["time"]),
                "game_score": self.safe_mean(game["answers"].astype(float))
            }

            # Testverhalten
            test = group[group["source"] == "test"].copy()
            test["difficulty"] = test["difficulty"].astype(float)
            test["time"] = test["time"].astype(float)

            test_features = {
                "test_difficulty_mean": self.safe_mean(test["difficulty"]),
                "test_difficulty_std": self.safe_std(test["difficulty"]),
                "test_time_mean": self.safe_mean(test["time"]),
                "test_time_std": self.safe_std(test["time"]),
                "test_score": self.safe_mean(test["answers"].astype(float))
            }

            # Fragebogen
            q = group[group["source"] == "questionnaire"].copy()
            q["answers"] = self.normalize_likert(q["answers"].astype(float))
            subscale_means = q.groupby("subscales")["answers"].mean().to_dict()
            questionnaire_score = np.mean([subscale_means.get(k, 0) for k in ["AAS", "PSC", "PC"]])

            profile = {
                "user_id": user_id,
                "name": name,
                **game_features,
                **test_features,
                **subscale_means,
                "questionnaire_score": questionnaire_score
            }

            profiles.append(profile)

        base_df = pd.DataFrame(profiles)
        #Test: print("Spalten im finalen Trainings-Datensatz:", base_df.columns.tolist())
        vector_df = VectorBuilder(base_df).build_vectors()
        distance_df = DistanceCalculator(vector_df).calc_distances()

        return pd.merge(base_df, distance_df, on=["user_id", "name"])
