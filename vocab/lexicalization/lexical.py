#!/usr/bin/env python
# coding: utf-8
from openai import OpenAI
from pydantic import BaseModel
import dspy

# import json

from ..preprocess.preprocess import (
    load_dictionary,
)


# Separate the Cambridge dictionary into training and develop dataset
def get_train_dev_set(dictionary):
    tmp_dict = dict(dictionary)
    cutpoint = len(tmp_dict) // 3
    ans_dict = {}
    for word in tmp_dict.keys():
        ch_def = []
        for pos in tmp_dict[word]:
            for big_sense_list in tmp_dict[word][pos]:
                for big_sense in big_sense_list["big_sense"]:
                    for sense in big_sense["sense"]:
                        ch_def.append(sense.pop("ch_def"))
        ans_dict[word] = ch_def

    trainset = {key: tmp_dict[key] for key in list(tmp_dict.keys())[:cutpoint]}
    devset = {key: tmp_dict[key] for key in list(tmp_dict.keys())[cutpoint:]}

    with open("./vocab/data/dspy/trainset.json", "w") as f:
        json.dump(trainset, f)
    with open("./vocab/data/dspy/devset.json", "w") as f:
        json.dump(devset, f)
    with open("./vocab/data/dspy/ans.json", "w") as f:
        json.dump(ans_dict, f)


def load_train_dev_set():
    trainset = None
    devset = None
    ans = None
    with open("./vocab/data/dspy/trainset.json", "r") as f:
        trainset = json.load(f)
    with open("./vocab/data/dspy/devset.json", "r") as f:
        devset = json.load(f)
    with open("./vocab/data/dspy/ans.json", "r") as f:
        ans = json.load(f)
    return trainset, devset, ans


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
