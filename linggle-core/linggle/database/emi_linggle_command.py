#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from .linggle_command import LinggleCommand

QUERY_RE = re.compile(r"\{[^}]+\}|\S+")
LONGEST_LEN = 5


class EmiLinggleCommand(LinggleCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.vocab:
            self.get_unigram = self.query

    def query(self, cmd):
        """return list of ngrams with counts"""

        # Deal with "$" in the query
        cmds = []
        if "$" in cmd:
            for word in cmd.split():
                if "$" in word:
                    new_word = EmiLinggleCommand.find_matches_in_file(word)

                    # print(f"(query) new_word: {new_word}")
                    # print(f"(query) cmd: {type(cmd)}, {cmd}")
                    # print(f"(query) word: {word}")
                    cmd = cmd.strip().replace(word, new_word)
            # print(f"(query) normalized_cmd: {cmd}")

        # Deal with ['/', '*', '~', '?', '{}'] in the query
        cmds = self.expand_query(cmd)
        # print(f"(query) final_cmds: {cmds}")
        return cmds

    @staticmethod
    def find_matches_in_file(patterns):
        # print(f"(find_matches_in_file) patterns: {patterns}")
        # Convert patterns to regex
        regex_patterns = EmiLinggleCommand.convert_dollar_to_regex(patterns)
        # print(f"(find_matches_in_file) regex_patterns: {regex_patterns}")

        # Read the file
        with open("./linggle/database/emi.vocab.txt", "r") as file:
            lines = file.readlines()

        # Find matches
        matches = ""
        for line in lines:
            word, count = line.split("\t")
            if re.search(regex_patterns, word):
                matches += (
                    "/" + line.split("\t")[0].strip()
                    if matches
                    else line.split("\t")[0].strip()
                )

        # print(f"(find_matches_in_file) matches: {matches}")
        return matches

    @staticmethod
    def convert_dollar_to_regex(token):
        # Find the position of the dollar sign
        dollar_pos = token.find("$")

        # Extract prefix and suffix
        prefix = token[:dollar_pos]
        suffix = token[dollar_pos + 1 :]

        # Construct regex token
        if prefix and suffix:
            regex_token = f"^{re.escape(prefix)}.*{re.escape(suffix)}$"
        elif prefix:
            regex_token = f"^{re.escape(prefix)}.*$"
        elif suffix:
            regex_token = f".*{re.escape(suffix)}$"
        else:
            regex_token = ".*"

        return regex_token
