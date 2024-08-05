#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from operator import itemgetter
from heapq import nlargest
from sqlitedict import SqliteDict
import logging
from .emi_vocab import VOCABULARY

from .emi_linggle_command import EmiLinggleCommand


# def expand_query(query):
#     """support for Common symbols in EMI.Linggle search"""
#     do_expand = EmiLinggleCommand(vocab=VOCABULARY)
#     queries = do_expand.query(query)
#     print(f"expand_queries: {queries}")
# for item in queries:
#     print(f"{item}")
# print("======end======")
# return queries


# def extend_query(query):
#     # TODO:
#     pass
#     return [query]


def load_database():
    logging.info("Loading...", end="")
    # read emi.linggle data
    # TODO:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "emiLinggle.db")
    dbLinggle = SqliteDict(db_path, tablename="query")
    logging.info("ready.")
    return dbLinggle


def linggle(db):
    q = input("emi.linggle> ")

    # exit execution keyword: exit()
    if q == "exit()":
        return

    # extend and expand query
    # queries = [
    #     simple_query
    #     for query in extend_query(q)
    #     for simple_query in expand_query(query)
    # ]
    do_expand = EmiLinggleCommand(vocab=VOCABULARY)
    queries = do_expand.query(q)
    print(f"expand_queries: {queries}")

    # gather results
    # try:
    #     ngramcounts = [item for query in queries for item in db[query]]
    # except KeyError:
    #     ngramcounts = list()

    ngramcounts = []
    for query in queries:
        try:
            items = db[query]
            ngramcounts.extend(items)
        except KeyError:
            continue

    # print(f"ngramcounts: {type(ngramcounts), ngramcounts}")

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
