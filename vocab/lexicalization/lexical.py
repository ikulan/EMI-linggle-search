#!/usr/bin/env python
# coding: utf-8
from openai import OpenAI
from pydantic import BaseModel
import dspy

# import json

from ..preprocess.preprocess import (
    load_dictionary,
    get_word_and_sense,
    load_train_dev_set,
)

client = OpenAI(api_key="$OPENAI_API_KEY")


class Senses(BaseModel):
    english_sense: str
    chinese_word: str


class LexicalizeSenseUseGPT(BaseModel):
    word: list[Senses]


def chat(target_word, word_dict):
    """ """
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
         You are a senior translator specializing in English to Traditional Mandarin Chinese.
         Task:
         Given an English word along with its definition. Each definition is divided by comma.
         Provide one precise and nuanced translation only for each definition.
         """,
            },
            {
                "role": "user",
                "content": f"""
         Word: {target_word},
         Definition: {word_dict[target_word]}
         """,
            },
        ],
        response_format=LexicalizeSenseUseGPT,
    )

    return completion.choices[0].message


class LexicalizeSenseUseDspy(dspy.Signature):
    word = dspy.InputField(
        desc="You are a senior translator specializing in English to Traditional Mandarin Chinese. Given an English word along with its definition."
    )
    word_senses = dspy.InputField(desc="Each definition is divided by comma.")

    lexicon = dspy.OutputField(
        desc="Provide one precise and nuanced translation only for each definition."
    )


class RAG(dspy.Module):
    def __init__(self, num_examples=5):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=num_examples)
        self.generate_answer = dspy.Predict(LexicalizeSenseUseDspy)

    def forward(self, question):
        context = self.retrieve(question)
        prediction = self.generate_answer(context=context, answer=question)
        return dspy.Prediction(context=context, answer=prediction.answer)


if __name__ == "__main__":
    cam_dict = load_dictionary("cambridge")
    web_dict = load_dictionary("mw")

    # Get the word and its senses
    word_sense_cam = {}
    word_sense_web = {}
    word_sense_cam = get_word_and_sense("ugly", cam_dict, word_sense_cam)
    word_sense_web = get_word_and_sense("ugly", web_dict, word_sense_web)

    # Lexicalization using GPT-4o-mini
    # gpt_lexicalized_cam = chat("ugly", word_sense_cam)
    # print(gpt_lexicalized_cam)
    # gpt_lexicalized_web = chat("ugly", word_sense_web)
    # print(gpt_lexicalized_web)

    # Lexicalization using DSPy

    # Only call model
    # gpt4o_mini = dspy.OpenAI("gpt-4o-mini", max_tokens=300)
    # dspy.configure(lm=gpt4o_mini)
    # dspy_lexicalized_cam = dspy_lexicalizer(
    #     word="ugly", word_senses=str(word_sense_cam["ugly"])
    # )
    # print(dspy_lexicalized_cam)

    # Using RAG
    gpt4o_mini = dspy.OpenAI("gpt-4o-mini", max_tokens=300)
    # colbertv2_wiki17_abstracts = dspy.ColBERTv2(
    #     url="http://20.102.90.50:2017/wiki17_abstracts"
    # )
    dspy.configure(lm=gpt4o_mini, rm=cam_dict)

    # Loading the dataset
    trainset, devset, ans = load_train_dev_set()

    dspy_lexicalizer = dspy.Predict(LexicalizeSenseUseDspy)
