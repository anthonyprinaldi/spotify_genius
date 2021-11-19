import os
import sys
import pandas as pd

def main():
    all_files = os.listdir('albums/')

    for i, file in enumerate(all_files):
        if i == 0:
            df = pd.read_csv(os.path.join('albums', file), index_col=0)
        else:
            df = df.append(pd.read_csv(os.path.join('albums', file), index_col=0), ignore_index=True)

    df.to_csv('taylor_swift_tracks.csv')

if __name__ == "__main__":
    main()