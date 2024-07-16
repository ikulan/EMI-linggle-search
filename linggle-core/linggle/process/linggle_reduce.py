#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Counter
from itertools import groupby
from operator import itemgetter


def parse_line(line):
    # query, ngram, count = line.strip().split("\t")
    # return query, ngram, int(count)
    query, ngram, npos, count = line.strip().split("\t")
    return query, ngram, npos, int(count)


def linggle_reduce(iterable, topn=None):
    # group values with the same query
    for query, results in groupby(iterable, key=itemgetter(0)):
        # print("query: ", query, ", results: ", results)
        counter = Counter()
        # for _, ngram, count in results:
        # counter[ngram] += count
        # yield query, counter.most_common(topn)
        for _, ngram, npos, count in results:
            counter[ngram] += count
        yield query, npos, counter.most_common(topn)


if __name__ == "__main__":
    import fileinput
    import sys
    import json
    import csv

    iterable = map(parse_line, fileinput.input())
    spamwriter = csv.writer(sys.stdout, delimiter="\t")
    # for query, result in linggle_reduce(iterable):
    #     # spamwriter.writerow([query, json.dumps(result, ensure_ascii=False)])
    #     print(
    #         query,
    #         *(f"{ngram} {count}" for ngram, count in result),
    #         sep="\t",
    #     )
    for query, npos, result in linggle_reduce(iterable):
        # spamwriter.writerow([query, json.dumps(result, ensure_ascii=False)])
        print(
            query,
            *(f"{ngram}|||{npos} {count}" for ngram, count in result),
            sep="\t",
        )
