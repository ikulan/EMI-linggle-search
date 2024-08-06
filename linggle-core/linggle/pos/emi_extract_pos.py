#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import product
from collections import defaultdict
import re


ITEM_RE = re.compile(r"\(([^()]+)\)")
# WILDCARDS = (" _ ",)


# def is_wildcard(token):
#     return token in WILDCARDS or token.endswith(".")


def to_indice(token):
    end = 0
    # print(f"token: {token}")
    for match in ITEM_RE.finditer(token):
        # print(f"match: {match.start()}, {match.end()}")
        # if end < match.start():
        # print(f"token[end:match.start()]: {token[end:match.start()]}")
        # yield token[end : match.start()]
        # print(f"match.group(1): {match.group(1).strip()}")
        # if (
        #     match.group(1) == "_SP"
        #     or match.group(1) == "``"
        #     or match.group(1) == "c"
        #     or match.group(1) == ","
        #     or match.group(1) == "$"
        # ):
        # print(f"token: {token}")
        # print(f"match: {match.start()}, {match.end()}")
        # print(f"match.group(1): {match.group(1)}")
        yield match.group(1)
        # print(f"end: {end}, match.end(): {match.end()}")
        end = match.end()
    if end < len(token):
        # print(f"token[end:]: {token[end:]}")
        yield token[end:]
    # yield " _ "


def to_map(iterable):
    for line in iterable:
        ngram, count = line.strip().split("\t")
        tokens = ngram.split()
        # print(f"tokens: {tokens}")
        candidates = [list(to_indice(token)) for token in tokens][0]
        # print(f"candidates: {candidates}")
        yield candidates
        # ngram_text = " ".join(token_candidates[0] for token_candidates in candidates)

        # for query in to_linggle_query(candidates):
        #     if query != ngram_text:
        #         yield query, ngram_text, count


if __name__ == "__main__":
    import fileinput

    pos = []
    for items in to_map(fileinput.input()):
        # print(*items, sep="\t")
        # print(type(items))
        pos.extend(items)
        pos = set(pos)
        pos = list(pos)
        # pass
    pos.sort()
    print(*pos, sep="\n")
