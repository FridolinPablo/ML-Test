import createDataFrame as cdf

if __name__ == "__main__":
    df = cdf.createDataFrame()
    df.load_all_json()
    all_data = df.create_dataframe()
    df.save_dataframe(all_data)