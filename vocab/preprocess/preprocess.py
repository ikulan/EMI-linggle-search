#!/usr/bin/env python
# coding: utf-8
import re
import json
from bs4 import BeautifulSoup

# import json


# ## Preprocess dictionary


# #### Load dictionary
def load_dictionary(dictionary_name):
    data = None
    with open(f"./vocab/data/{dictionary_name}/{dictionary_name}.word.json") as f:
        data = json.load(f)
    return data


def convert_mw_xml_to_dict(soup, start_word, num_word, stop_word):
    """
    Get example sentences from the webster dictionary
    input:
      soup: BeautifulSoup object
      start_word: the word we want to start with
      num_word: number of words we want to get
      stop_word: the word we want to stop at
    output:
      output_dict: a dictionary contains the word and its example sentences
    """
    pattern = r"{ldquo}|{rdquo}|{it}|{phrase}|{/phrase}|{dx}|{/dx}|\[\=.*\]|\n"
    output_dict = {}
    word_count = 0
    find = False
    # Find all words that contain example sentence/phrase
    for word in soup.find_all("entry"):
        # Get the number of words we want
        if stop_word is not None and word.find("id").text == stop_word:
            break
        elif find and word_count == num_word:
            break

        # First, find the target word
        word_id = word.find("id").text
        if (not find) and (word_id != start_word):
            continue
        else:
            find = True

        # Find each definition of POS of the word
        pos = word.find_all("fl")
        big_sense_list = []
        output_dict[word_id] = {}
        for ele in pos:
            fl = ele.contents[0]
            output_dict[word_id][fl] = []

            definition = ele.find_next("def")  # big sense
            big_sense_list = []
            # Find senses for each definition
            senses = definition.find_all("sense")

            for content in senses:
                sense_dict = {}
                sense = content.find("dt")
                if sense.contents[0] == "\n":
                    sense = sense.find("un").contents[0]
                    sense = re.sub(pattern, "", sense)
                else:
                    sense = sense.contents[0]
                    sense = re.sub(pattern, "", sense)
                sense_dict["en_def"] = sense

                # Get example sentences
                examples = content.find_all("vi")
                exam_list = []
                if examples != []:
                    for sentence in examples:
                        example = re.sub(pattern, "", sentence.text)
                        example = example.replace(r"{/it}", "")
                        exam_dict = {"en": example}
                        exam_list.append(exam_dict)
                sense_dict["examples"] = exam_list

                big_sense_list.append({"sense": [sense_dict]})
            output_dict[word_id][fl].append({"big_sense": big_sense_list})

        word_count += 1
    return output_dict


def load_webster_dictionary(start_word, stop_word=None, num_word=0):
    file = None
    with open("./vocab/data/mw/mw-xml/LD_u.xml", "r") as f:
        file = f.read()
    soup = BeautifulSoup(file, "xml")
    output_dict = convert_mw_xml_to_dict(soup, start_word, num_word, stop_word)
    return output_dict


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


# #### Obtain target word and its senses
def get_word_and_sense(word, dictionary, word_sense):
    """
    Get the word and its sense from the dictionary
    input:
      word: the word we want to find
      dictionary: the dictionary that contains the word
      word_sense: a dictionary contains the word and its sense
    output:
      word_sense: a dictionary contains the word and its sense
    """
    senses = []
    for pos in dictionary[word]:
        for big_sense_list in dictionary[word][pos]:
            for big_sense in big_sense_list["big_sense"]:
                for sense in big_sense["sense"]:
                    senses.append(sense["en_def"])
    word_sense[word] = senses

    return word_sense


if __name__ == "__main__":
    cam_dict = load_dictionary("cambridge")
    web_dict = load_dictionary("mw")

    # with open("../data/mw/mw-json/mw.word.json", "w") as f:
    #     json.dump(web_dict, f)
    # get_train_dev_set(cam_dict)
