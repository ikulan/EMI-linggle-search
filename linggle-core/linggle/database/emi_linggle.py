#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter
from itertools import chain
from heapq import nlargest
import logging


def expand_query(query):
    for token in filter(None, query.split('/')):
        # TODO:
        pass
    return [query]

def extend_query(query):
    # TODO:
    pass
    return [query]

def load_data():
    logging.info("Loading...", end='')
    # read emi.linggle data
    # TODO:
    db = None
    logging.info("ready.")
    return db

def linggle(db):
    q = input("emi.linggle> ")

    # exit execution keyword: exit()
    if q == 'exit()':
        return

    # extend and expand query
    queries = [
        simple_query,
        for query in extend_query(q)
        for simple_query in expand_query(query)
    ]
    print(queries)
    # gather results
    ngramcounts = {item for query in queries for item in db[query]}
    # output 10 most common ngrams
    ngramcounts = nlargest(10, ngramcounts, key=itemgetter(1))

    if len(ngramcounts) > 0:
        print(*(f"{count:>2,}: {ngram}" for ngram, count in ngramcounts), sep='\n')
    else:
        print(' '*8, "no results.")

    return True

if __name__ == '__main__':
    db_emi = load_data()
    while linggle(db_emi):
        pass
    db_emi.close()