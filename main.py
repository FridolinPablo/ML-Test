from createDataFrame import createDataFrame
from buildTrainData import UserProfileBuilder

creator = createDataFrame()
creator.load_all_json('./data/')
merged_df = creator.create_dataframe()

builder = UserProfileBuilder(merged_df)
train_df = builder.build_profiles()
print("Spalten im finalen Trainings-Datensatz:", train_df.columns.tolist())
train_df.to_csv('./dataframes/train_data.csv', index=False)
