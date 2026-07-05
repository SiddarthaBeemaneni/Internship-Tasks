from model import load_data, clean_data, eda, train_model
if __name__ == "__main__":
    df = load_data()
    eda(df)
    df = clean_data(df)
    accuracy = train_model(df)
    print(f"Final accuracy: {accuracy:.2%}")
