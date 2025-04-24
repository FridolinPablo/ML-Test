import pandas as pd

class VectorBuilder:
    def __init__(self, profile_df):
        self.df = profile_df.copy()

    def build_vectors(self):
        score_cols = [col for col in self.df.columns if col.endswith("_score")]

        vectors = []

        for _, row in self.df.iterrows():
            user_id = row["user_id"]
            name = row["name"]
            vector = {col: row.get(col, 0) for col in score_cols}

            vectors.append({
                "user_id": user_id,
                "name": name,
                **vector
            })

        return pd.DataFrame(vectors)
