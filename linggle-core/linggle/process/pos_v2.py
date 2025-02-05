import spacy
import sys
import os
import io
from nltk.tokenize import sent_tokenize
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex
from tqdm import tqdm


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


def do_pos(iterable):
    # iterable = io.open(sys.stdin.fileno(), "rt")
    for line in iterable:
        if line := line.strip():
            for sent in sent_tokenize(line):
                if sent := sent.strip():
                    # print(
                    #     " ".join(f"{token.text}({token.tag_})" for token in nlp(sent))
                    # )
                    tokens = []
                    for token in nlp(sent):
                        text = token.text.lower()
                        if token.tag_ == ".":
                            tokens.append(f"{text}(SENT_CLS)")
                        elif token.tag_ != token.text:
                            tokens.append(f"{text}({token.tag_})")
                        elif token.tag_ == ",":
                            tokens.append(f"{text}(COMMA)")
                        elif token.tag_ == ":":
                            tokens.append(f"{text}(COLON)")
                    print(" ".join(tokens))
            # yield sent


if __name__ == "__main__":
    import fileinput

    iterable = map(str.strip, fileinput.input())
    # mode = sys.argv[1] if len(sys.argv) > 1 else ""
    # if mode == "pos":
    # nlp = spacy.load(os.environ.get("SPACY_MODEL", "en_core_web_md"))
    nlp = spacy.load("en_core_web_sm")
    nlp.tokenizer = custom_tokenizer(nlp)
    do_pos(tqdm(list(iterable)))
