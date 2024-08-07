import os
from pathlib import Path
from collections import Counter


VOCAB_FILE_PATH = os.path.join("emi.vocab.txt")


def parse_line(line):
    word, count = line.strip().split("\t")
    return word, int(count)


if Path(VOCAB_FILE_PATH).is_file():
    VOCABULARY = Counter(dict(map(parse_line, open(VOCAB_FILE_PATH))))
else:
    VOCABULARY = {}
