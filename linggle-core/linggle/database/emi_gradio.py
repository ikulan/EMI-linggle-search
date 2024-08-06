"""a Python script that implements a Gradio interface for the EMI.Linggle application."""

from operator import itemgetter
from heapq import nlargest
import gradio as gr
from .emi_vocab import VOCABULARY
from .emi_linggle_command import EmiLinggleCommand
from .emi_linggle import load_database

# Load the database
db = load_database()


def process_query(q):
    ngramcounts = []
    do_expand = EmiLinggleCommand(vocab=VOCABULARY)
    queries = do_expand.query(q)
    print(f"(EMI search) expand_queries: {queries}\n\n")

    for query in queries:
        try:
            if len(query.split()) == 1:
                with open("./linggle/database/emi.vocab.txt", "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        word, count = line.split("\t")
                        if word == query:
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
        result = "No results found."
    return result


# Create Gradio interface with custom layout
with gr.Blocks() as iface:
    gr.Markdown("# EMI.Linggle")

    with gr.Accordion("HELP", open=False):
        gr.Markdown(
            """
        ## Common symbols
        > Linggle supports a few symbols while performing search.

        >> ### /: Or
        >> Any collection of words.
        >> Example: "receive/accept education"

        >> ### $: 0 ~ many characters
        >> Any length of characters.
        >> Examples: "what are you $ing"

        >> ### _: 1 word
        >> Any single word.
        >> Examples: "she is _"

        >> ### *: 0 ~ many words
        >> Any number of words.
        >> Examples: "do you *"

        >> ### ?: Optional
        >> Return results with/without the word.
        >> Examples: "discuss ?about the issue"
        """
        )

        gr.Markdown("## Part Of Speech")

    gr.Markdown("Enter your query to get n-gram counts.")
    query_input = gr.Textbox(lines=1, placeholder="Input your query here...")
    query_button = gr.Button("Submit")
    query_output = gr.TextArea()

    query_button.click(fn=process_query, inputs=query_input, outputs=query_output)


if __name__ == "__main__":
    iface.launch()


# query = "you are res$ing at/in ?an"
# query = "you _ _ *"
# query = "are res$ing"
