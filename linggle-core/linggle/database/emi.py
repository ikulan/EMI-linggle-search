#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from operator import itemgetter
from heapq import nlargest
from sqlitedict import SqliteDict
import logging
from .emi_vocab import VOCABULARY

from .emi_command import EmiLinggleCommand
# from ..postgres.db import *

# connection = connect_to_db()
# cursor = connection.cursor()

def load_database():
    logging.info("Loading...", end="")
    # read emi.linggle data
    # TODO:
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = (
        "/home/nlplab/atwolin/EMI-linggle-search/linggle-core/linggle/database/"
    )
    db1_path = os.path.join(script_dir, "emi.db")
    db2_path = os.path.join(script_dir, "dictionary.db")
    db_yale = SqliteDict(db1_path, tablename="query")
    # db_dict = SqliteDict(db2_path, tablename="query")
    db_dict = None
    logging.info("ready.")
    return db_yale, db_dict


def process_query(q, db):
    ngramcounts = []
    do_expand = EmiLinggleCommand(vocab=VOCABULARY)
    queries = do_expand.query(q)
    # print(f"(EMI search) expand_queries: {queries}\n\n")

    # Gather results
    for query in queries:
        try:
            if len(query.split()) == 1:
                with open(
                    "/home/nlplab/atwolin/EMI-linggle-search/data/nc-vocab-out/vocab.merged.txt",
                    "r",
                ) as file:
                    lines = file.readlines()
                    for line in lines:
                        word, count = line.split("\t")
                        if word.startswith(query + "("):
                            ngramcounts.append((word, int(count)))
            else:
                items = db[query]
                ngramcounts.extend(items)
        except KeyError:
            continue

    ngramcounts = nlargest(50, ngramcounts, key=itemgetter(1))
    if len(ngramcounts) >> 0:
        result = "\n".join(f"{count:> 7,}: {ngram}" for ngram, count in ngramcounts)
    else:
        result = ""
    return result


def linggle(linggle_db, dict_db):
    q = input("emi.linggle> ")

    # exit execution keyword: exit()
    if q == "exit()":
        return False

    # Gather results
    result1 = process_query(q, linggle_db)
    # result2 = process_query(q, dict_db)

    # if (result1 == "") and (result2 == ""):
    if (result1 == ""):
        print("No results found.")
    else:
        print("In yale:")
        print(result1)
        # print("In dictionaries:")
        # print(result2)

    return True


if __name__ == "__main__":
    db_yale = load_database()
    if db_yale is None:
        raise ValueError("Failed to load db_yale")
    db_yale, db_dict = load_database()
    while linggle(db_yale, db_dict):
        pass
    db_yale.close()
    db_dict.close()
