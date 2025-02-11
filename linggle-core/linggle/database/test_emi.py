#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sqlitedict import SqliteDict
from pprint import pprint

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "emi.db")

dbLinggle1 = SqliteDict(db_path, tablename="query")
ngram = "if we"
test = dbLinggle1[ngram]
print(f"key: {ngram}\n")
pprint(test)
# print("There are %d items in the database" % len(dbLinggle1))
