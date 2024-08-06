#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import os
# from sqlitedict import SqliteDict

# script_dir = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(script_dir, "emiLinggle.db")

# dbLinggle1 = SqliteDict(db_path, tablename="query")
# ngram = "this NN"
# test = dbLinggle1[ngram]
# print(test)
# print("There are %d items in the database" % len(dbLinggle1))

import re


def convert_dollar_to_regex(query):
    # Replace $ with .*
    return re.sub(r"\$", r".*", query)


def find_matches_in_file(patterns, filename):
    # Convert patterns to regex
    regex_patterns = [convert_dollar_to_regex(pattern) for pattern in patterns]

    # Read the file
    with open(filename, "r") as file:
        lines = file.readlines()

    # Find matches
    matches = {pattern: [] for pattern in patterns}
    for line in lines:
        for pattern, regex in zip(patterns, regex_patterns):
            if re.search(regex, line):
                matches[pattern].append(line.strip())

    return matches


# Patterns to search for
patterns = ["$ing", "w$n", "$melon"]

# Find matches in emi_vocab.txt
matches = find_matches_in_file(patterns, "emi.vocab.txt")

# Print the matches
for pattern, matched_lines in matches.items():
    print(f"Pattern: {pattern}")
    for line in matched_lines:
        print(f"  Match: {line}")
