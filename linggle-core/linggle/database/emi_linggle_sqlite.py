"""Create a database that contains ngram count for yale transcripts."""

from sqlitedict import SqliteDict
from tqdm import tqdm

db = SqliteDict("emiLinggle.db", tablename="query", autocommit=True)


def parse_ngramstr(text):
    ngram_pos, count = text.rsplit(" ", maxsplit=1)
    ngram, pos = ngram_pos.rsplit("|||", maxsplit=1)
    return ngram, pos, int(count)


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
        # print(f"key: {key}, value: {value}")
        # pass
    return None


if __name__ == "__main__":
    import fileinput

    load_ngram(fileinput.input())
