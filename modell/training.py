import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
import matplotlib.pyplot as plt

df = pd.read_csv("daten.csv")

# Zielspalten definieren
target_columns = ["score_problemlösen", "score_frustration"]

# Features: alle anderen numerischen Spalten außer den Zielspalten
X = df.drop(columns=target_columns)
y = df[target_columns]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Basismodell
rf = RandomForestRegressor(n_estimators=100, random_state=42)

# MultiOutput-Hülle
multi_rf = MultiOutputRegressor(rf)

# Modell trainieren
multi_rf.fit(X_train, y_train)

predictions = multi_rf.predict(X_test)

from sklearn.metrics import mean_squared_error

for i, col in enumerate(target_columns):
    mse = mean_squared_error(y_test[col], predictions[:, i])
    print(f"{col} - MSE: {mse:.2f}")
    
importances = multi_rf.estimators_[0].feature_importances_
feat_names = X.columns
sorted_idx = importances.argsort()

plt.barh(feat_names[sorted_idx], importances[sorted_idx])
plt.title("Feature Importance (für erstes Ziel)")
plt.show()