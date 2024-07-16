import re

from .linggle_command import LinggleCommand
from .emi_vocab import VOCABULARY

QUERY_RE = re.compile(r"\{[^}]+\}|\S+")
LONGEST_LEN = 5


class emiLinggleCommand(LinggleCommand):
    def __init__(
        self, *args, find_synonyms=None, word_delimiter=" ", vocab=VOCABULARY, **kwargs
    ):
        if find_synonyms:
            self.find_synonyms = find_synonyms
        self.word_delimiter = word_delimiter
        self.vocab = vocab
