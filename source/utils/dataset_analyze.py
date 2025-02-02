from pathlib import Path

import chardet
import pandas as pd

from ..config import Settings

settings = Settings()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / f"books_data/{settings.INPUT_FILE}"

settings = Settings()


def main():
    df = pd.read_csv(
        DATA_FILE, header=0, encoding="ISO-8859-1", on_bad_lines="skip", sep=";"
    )

    print(f"Columns: {df, columns}")

    for field in list(df.columns):
        print(field)
        longest_index = df[field].str.len().idxmax()
        print(f"Length: {len(df.loc[longest_index, field])}")

    with open(DATA_FILE, "rb") as f:
        raw_data = f.read(10000)
        result = chardet.detect(raw_data)
        print(result)


if __name__ == "__main__":
    main()
