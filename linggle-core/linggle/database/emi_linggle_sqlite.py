"""Create a database that contains ngram count for yale transcripts."""
from sqlitedict import SqliteDict

db = SqliteDict('emiLinggle.db', autocommit=True)


def parse_ngramstr(text):
    ngram, count = text.rsplit(" ", maxsplit=1)
    ngram, pos = ngram.rsplit("|||", maxsplit=1)
    # print(f"parse_ngramstr: {ngram} ||||||| {count}")
    # for text in ngram:
        # print(f"text: {type(text)}, {text}")
    # print(f"n: {n}, pos: {pos}")
    return ngram, pos, int(count)

def parse_line(line):
    query, *ngramcounts = line.strip().split("\t")
    # print(f"parse_line: {query} ||||||| {ngramcounts}")
    # for text in ngramcounts:
    #     print(f"text: {type(text)}, {text}")
    return query, tuple(map(parse_ngramstr, ngramcounts))

def load_data(lines):
    # TODO:
    for query, ngramcounts in map(parse_line, lines):
        # print(f"ngramcounts: {ngramcounts}")
        db[query] = ngramcounts
    return None

if __name__ == '__main__':
    import fileinput
    load_data(fileinput.input())