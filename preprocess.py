import argparse
import json
import os
import pandas as pd


def read_data(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    if os.path.exists(path + '.xz'):
        return pd.read_csv(path + '.xz', compression='xz')
    raise FileNotFoundError(path)


def main():
    p = argparse.ArgumentParser(description='Preprocess Goodreads data')
    p.add_argument('-i', '--input', default='GoodReads_100k_books.csv')
    p.add_argument('-o', '--output', default='scatter_data.json')
    args = p.parse_args()

    df = read_data(args.input)

    df['pages'] = pd.to_numeric(df['pages'], errors='coerce')
    df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['blurb'] = df['desc'].fillna('').astype(str).str.len()
    df = df[['pages', 'blurb', 'reviews', 'rating']].dropna()

    for col in df.columns:
        low, high = df[col].quantile([0.005, 0.995])
        df = df[(df[col] >= low) & (df[col] <= high)]

    df = df.sample(n=min(5000, len(df)), random_state=42)

    with open(args.output, 'w') as f:
        json.dump(df.to_dict(orient='records'), f, separators=(',', ':'))

    size = os.path.getsize(args.output)
    print(size)


if __name__ == '__main__':
    main()
