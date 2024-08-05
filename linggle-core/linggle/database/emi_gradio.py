"""a Python script that implements a Gradio interface for the EMI.Linggle application."""

from operator import itemgetter
from heapq import nlargest
import gradio as gr
from .emi_vocab import VOCABULARY
from .emi_linggle_command import EmiLinggleCommand
from .emi_linggle import load_database

# Load the database
db = load_database()


def process_query(query):
    expand_query = EmiLinggleCommand(vocab=VOCABULARY)
    queries = expand_query.query(query)
    ngramcounts = []
    for query in queries:
        try:
            items = db[query]
            ngramcounts.extend(items)
        except KeyError:
            continue

    ngramcounts = nlargest(50, ngramcounts, key=itemgetter(1))
    if len(ngramcounts) > 0:
        result = "\n".join(f"{count:>7,}: {ngram}" for ngram, pos, count in ngramcounts)
    else:
        result = "No results found."
    return result


# Create Gradio interface
iface = gr.Interface(
    fn=process_query,
    inputs=gr.Textbox(lines=2, placeholder="Input your query here..."),
    outputs="text",
    title="EMI.Linggle",
    description="Enter your query to get n-gram counts.",
    theme=gr.themes.Monochrome(text_size="lg", spacing_size="lg"),
    # css="style.css",
)

if __name__ == "__main__":
    iface.launch()
