import pandas as pd
import numpy as np
from itertools import combinations

class DistanceCalculator:
    def __init__(self, vector_df):
        self.df = vector_df.copy()

    def calc_distances(self):
        results = []
        score_cols = [col for col in self.df.columns if col.endswith("_score")]

        for _, row in self.df.iterrows():
            user_id = row["user_id"]
            name = row["name"]

            base_vectors = {}
            for i, col in enumerate(score_cols):
                vec = np.zeros(len(score_cols))
                vec[i] = row[col]
                base_vectors[col] = vec

            pairwise_distances = {}
            for a, b in combinations(score_cols, 2):
                dist = np.linalg.norm(base_vectors[a] - base_vectors[b])
                key = f"dist_{a.replace('_score','')}_{b.replace('_score','')}"
                pairwise_distances[key] = dist

            weight = 1 / (pairwise_distances.get("dist_game_test", 1e-6) + 1e-6)

            results.append({
                "user_id": user_id,
                "name": name,
                **pairwise_distances,
                "sample_weight": weight
            })

        return pd.DataFrame(results)
