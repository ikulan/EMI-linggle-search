#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import product
import re


ITEM_RE = re.compile(
    r"\(([^()]+)\)?"
)  # add (), the word within the () can be searched. e.g. pos
WILDCARDS = (" _ ",)


def get_pure_text(ngram):
    # print(f"ngram: {type(ngram)}")
    return (
        token.split("||", 1)[0] if token.rfind("||", 1) else token
        for token in ngram.split()
    )


def get_pos(ngram):
    return (
        token.split("||", 1)[1][:-2] if token.rfind("||", 1) else token
        for token in ngram.split()
    )


def is_wildcard(token):
    return token in WILDCARDS or token.endswith(".")


def to_indice(token):
    yield " _ "
    end = 0
    for match in ITEM_RE.finditer(token):
        if end < match.start():
            yield token[end : match.start()]
        yield f" {match.group(1)} "
        end = match.end()
    if end < len(token):
        yield token[end:]


def to_linggle_query(tokens, delim=" "):
    ngram_text = list(get_pure_text(tokens))
    # candidates = [list(to_indice(token)) for token in tokens]
    candidates = [list(to_indice(token)) for token in ngram_text]
    for query_tokens in product(*candidates):
        # skip queries consisting of wildcards only
        # if not all(is_wildcard(token) for token in query_tokens):
        # remove redundant spaces
        yield " ".join(delim.join(query_tokens).split())


def linggle_map(iterable):
    for line in iterable:
        # print(f"line: {line}")
        # ngram, npos, count = line.strip().split("\t")
        ngram, count = line.strip().split("\t")
        # print(f"ngram: {ngram}, count: {count}")
        ngram_text = " ".join(get_pure_text(ngram))
        npos = " ".join(get_pos(ngram))
        # tokens = ngram.split()
        # print(f"tokens: {tokens}")

        # print(list(token.split("(", 1) if token.rfind("(", 1) else token for token in tokens))
        # print(f"ngram_text: {ngram_text}, npos: {npos}")
        # print("=======================================")
        # for query in to_linggle_query(tokens):
        for query in to_linggle_query(ngram):
            if query != ngram_text:
                yield query, ngram_text, npos, count
                # yield query, ngram_text, count


if __name__ == "__main__":
    import fileinput

    for items in linggle_map(fileinput.input()):
        # print(*items, sep="\t")
        pass
