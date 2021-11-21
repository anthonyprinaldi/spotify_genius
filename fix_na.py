import pandas as pd
from get_taylor import scrape_lyrics


def main():
    final_df = pd.read_csv("taylor_swift_tracks.csv", index_col=0)
    for i in range(final_df.shape[0]):
        if pd.isna(final_df.lyrics[i]):
            print(f"Retrying for {final_df.track[i]}")
            final_df.loc[final_df.index[i], "lyrics"] = scrape_lyrics(
                "taylor swift", final_df.track[i]
            )
    final_df.to_csv("tracksV2.csv")
    return None


if __name__ == "__main__":
    main()
