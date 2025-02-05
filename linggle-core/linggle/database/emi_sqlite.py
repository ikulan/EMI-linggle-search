"""Create a database that contains ngram count for yale transcripts."""

from sqlitedict import SqliteDict
from tqdm import tqdm

db = SqliteDict(
    "/home/nlplab/atwolin/EMI-linggle-search/linggle-core/linggle/database/dictionary.db",
    tablename="query",
    autocommit=True,
)


def parse_ngramstr(text):
    ngram, count = text.rsplit(" ", maxsplit=1)
    return ngram, int(count)


def parse_line(line):
    query, *ngramcounts = line.strip().split("\t")
    return query, tuple(map(parse_ngramstr, ngramcounts))


def load_ngram(lines):
    # TODO:
    # read linggle data
    linggle_table = {
        query: ngramcounts for query, ngramcounts in map(parse_line, lines)
    }
    for key, value in tqdm(linggle_table.items()):
        db[key] = value  # key: query, value: ngram, npos, counts
        # print(f"key: {key},\nvalue: {value}")
        # pass
    return None


if __name__ == "__main__":
    import fileinput

    print("Loading...")
    load_ngram(fileinput.input())
    print("ready.")
