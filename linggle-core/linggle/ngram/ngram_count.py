#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from itertools import groupby
import spacy
import sys
import os
import io
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex


nlp = None


def ngram_is_valid(ngram):
    if any(
        (token.is_punct and (token.text != ",")) or token.is_digit for token in ngram
    ):
        return False
    return True


def to_ngrams(doc, n):
    for i in range(len(doc) - n + 1):
        yield doc[i : i + n]


def sentence_to_ngrams(doc):
    for n in range(1, 6):
        for ngram in to_ngrams(doc, n):
            if ngram_is_valid(ngram):
                yield ngram


def normalize_sent(sent):
    return " ".join(sent.split())


def custom_tokenizer(nlp):
    inf = list(nlp.Defaults.infixes)  # Default infixes
    inf.remove(
        r"(?<=[0-9])[+\-\*^](?=[0-9-])"
    )  # Remove the generic op between numbers or between a number and a -
    inf = tuple(inf)  # Convert inf to tuple
    infixes = inf + tuple(
        [r"(?<=[0-9])[+*^](?=[0-9-])", r"(?<=[0-9])-(?=-)"]
    )  # Add the removed rule after subtracting (?<=[0-9])-(?=[0-9]) pattern
    infixes = [
        x for x in infixes if "-|–|—|--|---|——|~" not in x
    ]  # Remove - between letters rule
    infix_re = compile_infix_regex(infixes)

    return Tokenizer(
        nlp.vocab,
        prefix_search=nlp.tokenizer.prefix_search,
        suffix_search=nlp.tokenizer.suffix_search,
        infix_finditer=infix_re.finditer,
        token_match=nlp.tokenizer.token_match,
        rules=nlp.Defaults.tokenizer_exceptions,
    )


def map_ngrams(iterable):
    def chunk_str(token):
        if token.i + 1 in invalid_bound:
            return ""
        elif token.i in np_head_i:
            return "NP"
        else:
            return token.tag_

    # iterable = fileinput.input()
    for sent in map(normalize_sent, iterable):
        nlp.tokenizer = custom_tokenizer(nlp)
        doc = nlp(sent)
        # print("doc: ", doc)
        # print("hi: ", [token for token in doc])
        # print("doc.noun_chunks: ", list(doc.noun_chunks))
        np_head_i = {chunk.end - 1 for chunk in doc.noun_chunks}
        invalid_bound = {
            i for chunk in doc.noun_chunks for i in range(chunk.start + 1, chunk.end)
        }

        for ngram in sentence_to_ngrams(doc):
            ngram_str = ngram.text.strip()

            tags = []
            for token in ngram:
                if token.text == ",":
                    tags.append("COMMA")
                    continue
                tags.append(token.tag_)
            npos_str = " ".join(tags)
            # npos_str = " ".join(token.tag_ for token in ngram)

            nchunk_str = ""
            if not (ngram.start in invalid_bound or ngram.end in invalid_bound):
                nchunk_str = " ".join(chunk_str(token) for token in ngram)

            # print("ngram_str: ", ngram_str, "; npos_str: ", npos_str)
            # yield ngram_str, npos_str
            yield ngram_str, npos_str, nchunk_str


def parse_reduce_input(line):
    line = line.strip("\r\n")
    # [tuple(item.split(' ')) for item in line.split('\t')]
    ngram, npos = line.split("\u3000")
    return ngram, npos
    # ngram, npos, nchunk = line.split("\u3000")
    # return ngram, npos, nchunk


def reduce_ngrams(ngrams):
    # info = Counter()

    for (ngram, npos), items in groupby(ngrams):
        count = sum(1 for _ in items)
        yield ngram, npos, count

    # for (ngram, npos, nchunk), items in groupby(ngrams):
    #     count = sum(1 for _ in items)
    #     yield ngram, npos, nchunk, count

    # for _, npos, nchunk in items:
    #     info[npos, nchunk] += 1
    # for (npos, nchunk), count in info.most_common():
    #     print(ngram, npos, nchunk, count, sep='\t')
    # info.clear()


def do_pos():
    iterable = io.open(sys.stdin.fileno(), "rt")
    for ngram, npos, nchunk in map_ngrams(iterable):
        print(f"{ngram}({npos})")


def do_map():
    iterable = io.open(sys.stdin.fileno(), "rt")
    # for ngram, npos in map_ngrams(iterable):
    # print(ngram, npos, sep="\u3000")
    for ngram, npos, nchunk in map_ngrams(iterable):
        print(ngram, npos, sep="\u3000")
        # print(ngram, npos, nchunk, sep="\u3000")


def do_reduce():
    iterable = io.open(sys.stdin.fileno(), "rt")
    ngrams = map(parse_reduce_input, iterable)
    for ngram, npos, count in reduce_ngrams(ngrams):
        print(ngram, npos, count, sep="\t")
    # for ngram, npos, nchunk, count in reduce_ngrams(ngrams):
    #     print(ngram, npos, nchunk, count, sep="\t")
    # for _, npos, nchunk in items:
    #     info[npos, nchunk] += 1
    # for (npos, nchunk), count in info.most_common():
    #     print(ngram, npos, nchunk, count, sep='\t')
    # info.clear()
    # uniq -c


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "pos":
        nlp = spacy.load(os.environ.get("SPACY_MODEL", "en_core_web_md"))
        do_pos()
    elif mode == "map":
        # load spacy model
        nlp = spacy.load(os.environ.get("SPACY_MODEL", "en_core_web_md"))
        do_map()
    elif mode == "reduce":
        do_reduce()
    else:
        from collections import Counter

        nlp = spacy.load(os.environ.get("SPACY_MODEL", "en_core_web_md"))
        iterable = io.open(sys.stdin.fileno(), "rt")
        ngram_count = Counter(map_ngrams(iterable))
        for (ngram, npos, nchunk), count in ngram_count.most_common():
            # print(ngram, npos, nchunk, count, sep="\t")
            print(ngram, npos, count, sep="\t")
