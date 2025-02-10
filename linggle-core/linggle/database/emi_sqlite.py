"""Create a database that contains ngram count for yale transcripts."""

from sqlitedict import SqliteDict
from tqdm import tqdm


def parse_ngramstr(text):
    ngram, count = text.rsplit(" ", maxsplit=1)
    return ngram, int(count)


def parse_line(line):
    query, *ngramcounts = line.strip().split("\t")
    return query, tuple(map(parse_ngramstr, ngramcounts))


def load_ngram(lines, db_path):
    # TODO:
    # read linggle data
    print(f"Using database: {db_path}")
    with SqliteDict(db_path, tablename="query", autocommit=True) as db:
        linggle_table = {
            query: ngramcounts for query, ngramcounts in map(parse_line, lines)
        }
        for key, value in tqdm(linggle_table.items()):
            db[key] = value  # key: query, value: ngram, npos, counts
            # print(f"key: {key},\nvalue: {value}")
            # pass
        return None


if __name__ == "__main__":
    import argparse
    import fileinput 

    parser = argparse.ArgumentParser(description="Load Linggle data into SQLite database.")
    parser.add_argument(
        "db_path", type=str, help="Path to the SQLite database file."
    )
    parser.add_argument(
        "input_files", nargs="+", help="One or more input files to process."
    )    
    args = parser.parse_args()

    print("Loading...")
    load_ngram(fileinput.input(args.input_files), args.db_path)
    print("ready.")
