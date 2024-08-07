#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from sqlitedict import SqliteDict
from pprint import pprint

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "emiLinggle.db")

dbLinggle1 = SqliteDict(db_path, tablename="query")
ngram = "that _ the _"
test = dbLinggle1[ngram]
print(f"key: {ngram}\n")
pprint(test)
# print("There are %d items in the database" % len(dbLinggle1))
