#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter
from itertools import chain
from heapq import nlargest
from sqlitedict import SqliteDict
import logging

# from emi_linggle_command import emiLinggleCommand


def expand_query(query):
    """support for Common symbols in EMI.Linggle search"""
    for token in filter(None, query.split("/")):
        # TODO:
        pass
    return [query]


def extend_query(query):
    # TODO:
    pass
    return [query]


def load_database():
    logging.info("Loading...", end="")
    # read emi.linggle data
    # TODO:
    dbLinggle = SqliteDict("emiLinggle.db", tablename="query", autocommit=True)
    logging.info("ready.")
    return dbLinggle


def linggle(db):
    q = input("emi.linggle> ")

    # exit execution keyword: exit()
    if q == "exit()":
        return

    # extend and expand query
    queries = [
        simple_query
        for query in extend_query(q)
        for simple_query in expand_query(query)
    ]
    # print(f"queries: {queries}")
    # gather results
    try:
        ngramcounts = {item for query in queries for item in db[query]}
    except:
        ngramcounts = set()
    # output 10 most common ngrams
    ngramcounts = nlargest(10, ngramcounts, key=itemgetter(1))
    # print(f"ngramcounts: {ngramcounts}")
    if len(ngramcounts) > 0:
        print(*(f"{count:>7,}: {ngram}" for ngram, pos, count in ngramcounts), sep="\n")
    else:
        print(" " * 8, "no results.")

    return True


if __name__ == "__main__":
    db_emi = load_database()
    while linggle(db_emi):
        pass
    db_emi.close()
