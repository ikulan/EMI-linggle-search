#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import groupby
from linggle_map import get_pure_text


def parse_line(iterable):
    for line in iterable:
        ngram, count = line.strip().split("\t")
        ngram_text = list(get_pure_text(ngram))[0]
        yield ngram_text, count


if __name__ == "__main__":
    import fileinput

    for ngram, count in parse_line(fileinput.input()):
        print(ngram, count, sep="\t")
        # print(" ".join(get_pure_text(ngram[0])),
