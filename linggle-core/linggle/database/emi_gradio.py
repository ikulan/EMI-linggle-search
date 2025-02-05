"""a Python script that implements a Gradio interface for the EMI.Linggle application."""

from operator import itemgetter
from heapq import nlargest
import gradio as gr
from .emi_vocab import VOCABULARY
from .emi_command import EmiLinggleCommand
from .emi import load_database, process_query

# Load the database
db = load_database()


# Create Gradio interface with custom layout
with gr.Blocks(
    theme="finlaymacklon/boxy_violet",
) as iface:
    gr.Markdown("# E.M.I.ighty")

    with gr.Accordion("HELP", open=False):
        gr.Markdown(
            """
        ## **Common symbols**
        > Linggle supports a few symbols while performing search.

        `/` Or \\
        Any collection of words. \\
        Example: `receive/accept`

        `$` 0 ~ many characters \\
        Any length of characters. \\
        Examples: `what are you $ing`

        `_` 1 word \\
        Any single word. \\
        Examples: `she is _`

        `*` 0 ~ many words \\
        Any number of words. \\
        Examples: `do you *`

        `?` Optional \\
        Return results with/without the word. \\
        Examples: `discuss ?about`

         \\
        ## **Part Of Speech**
        ADD
        AFX
        C
        CC
        CD
        COLON
        COMMA
        DT
        EX
        FW
        G
        HYPH
        IN
        JJ
        JJR
        JJS
        LS
        MD
        NFP
        NN
        NNP
        NNPS
        NNS
        PDT
        POS
        PRP
        PRP$
        RB
        RBR
        RBS
        RP
        SENT_CLS
        SYM
        TO
        UH
        VB
        VBD
        VBG
        VBN
        VBP
        VBZ
        WDT
        WP
        WP$
        WRB
        """
        )

    gr.Markdown("Enter your query to get n-gram counts.")
    query_input = gr.Textbox(
        lines=1, value="if PRP look at", placeholder="Input your query here..."
    )
    query_button = gr.Button("Submit")
    query_output = gr.TextArea()

    query_button.click(fn=process_query, inputs=query_input, outputs=query_output)


if __name__ == "__main__":
    iface.launch(share=True)
    # iface.launch()


# query = "you are res$ing at/in ?an"
# query = "you _ _ *"
# query = "are res$ing"
