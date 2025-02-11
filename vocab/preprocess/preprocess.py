#!/usr/bin/env python
# coding: utf-8
import re
import json
from bs4 import BeautifulSoup


# Process Merriam-Webster dictionary
def load_webster_dictionary(letter):
    file = None
    with open(f"./vocab/data/mw/mw-xml/LD{letter}.xml", "r") as f:
        file = f.read()
    soup = BeautifulSoup(file, "xml")
    return soup


def convert_mw_xml_format(word, word_id):
    """
    Transform the Merriam-Webster XML file to cambridge-format dictionary
    input:
      soup: BeautifulSoup object
      word: the word we want to convert its format
    output:
      output_dict: a dictionary contains the word and its example sentences
    """
    pattern = r"\{bc\}|{ldquo}|{rdquo}|{it}|{phrase}|{/phrase}|{dx}|{/dx}|\[\=.*\]|\n"
    add_period = r"\ \{bc\}"
    output_dict = {}

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
        if definition is None:
            continue
        senses = definition.find_all("sense")

        for content in senses:
            # Get senses of the word
            sense_dict = {}
            sense = content.find("dt")
            # print(f"Before: {sense}")
            if sense.contents[0] == "\n":
                if sense.find("un") is None:
                    snote = sense.find("snote")
                    t_tags = snote.find_all("t")
                    vis = t_tags[0].find_next_siblings("vis")
                    idx = 0
                    for t_tag in t_tags:
                        sub_sense_dict = {}
                        if t_tag.find_next_siblings("vis") == []:
                            continue
                        t_tag = re.sub(pattern + "", "", t_tag.text)
                        t_tag = re.sub(add_period, ". ", t_tag)
                        sub_sense_dict["en_def"] = t_tag

                        # print(f"\n\nt_tag: {t_tag}\n")
                        # print(f"vis: {vis[idx]}\n")
                        exam_list = []
                        for sentence in vis[idx]:
                            if sentence == "\n":
                                continue
                            # print(f"sentence: {sentence}\n")
                            example = re.sub(pattern, "", sentence.text)
                            example = example.replace(r"{/it}", "")
                            exam_dict = {"en": example}
                            exam_list.append(exam_dict)
                        # print(f"exam_list: {exam_list}\n")
                        sub_sense_dict["examples"] = exam_list

                        big_sense_list.append({"sense": [sub_sense_dict]})
                        idx += 1
                    output_dict[word_id][fl].append({"big_sense": big_sense_list})
                    # print(f"\n\noutput_dict[{word_id}]: {output_dict[word_id]}\n")
                    # assert False
                    continue
                sense = sense.find("un").contents[0]

            else:
                sense = sense.contents[0]
            # print(f"Extract: {sense}")
            sense = re.sub(pattern, "", sense.text)
            sense = re.sub(add_period, ". ", sense)
            # print(f"After: {sense}")
            sense_dict["en_def"] = sense

            # Get examples sentences
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

    return output_dict


def convert_words_from_mw_xml(soup):
    """
    Get all words and their content from the Merriam-Webster XML file
    input:
      soup: BeautifulSoup object
    output:
      words: a dictionary stores words and their content
    """
    words = dict()
    for word in soup.find_all("entry"):
        # First, find the target word
        word_id = word.find("id").text

        # Start converting the word
        words.update(convert_mw_xml_format(word, word_id))

    return words


def convert_specific_mw_xml_to_dict(soup, start_word, num_word, stop_word):
    """
    Transform the Merriam-Webster XML file to cambridge-format dictionary
    input:
      soup: BeautifulSoup object
      start_word: the word we want to start with
      num_word: number of words we want to get
      stop_word: the word we want to stop at
    output:
      output_dict: a dictionary contains the word and its example sentences
    """
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

        # Start converting the word
        output_dict.update(convert_mw_xml_format(word, word_id))

        word_count += 1
    return output_dict


# Load json format dictionary
def load_dictionary(dictionary_name):
    data = None
    with open(f"./vocab/data/{dictionary_name}/{dictionary_name}.word.json") as f:
        data = json.load(f)
    return data


# Process json format dictionary
def get_sepecific_word_and_sense(word, dictionary, word_sense):
    """
    Get the target word and its sense from the dictionary
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


def get_examples(dictionary):
    """
    Get examples from the dictionary (json format)
    input:
        dictionary: the dictionary we want to get examples from
    output:
        examples: a list of all examples in the dictionary
    """
    examples = []
    for word in dictionary.keys():
        for pos in dictionary[word]:
            for big_sense_list in dictionary[word][pos]:
                for big_sense in big_sense_list["big_sense"]:
                    for sense in big_sense["sense"]:
                        for content in sense["examples"]:
                            example = content["en"]
                            examples.append(example)
    return examples


def store_examples(dictionary, filename):
    """
    Store examples to a file
    input:
        dictionary: the dictionary we want to get examples from (json format)
        filename: the text file we want to store the examples
    """
    examples = get_examples(dictionary)
    with open(filename, "w") as f:
        for example in examples:
            f.write(f"{example}\n")


if __name__ == "__main__":
    # cam_dict = load_dictionary("cambridge")

    # Preprocess the Merriam-Webster dictionary
    # web_dict = dict()
    alphbat = [
        "_a",
        "_b",
        "_c",
        "_d",
        "_e",
        "_f",
        "_g",
        "_h",
        "_i",
        "_j",
        "_k",
        "_l",
        "_m",
        "_n",
        "_o",
        "_p",
        "_q",
        "_r",
        "_s1",
        "_s2",
        "_t",
        "_u",
        "_v",
        "_w",
        "_x",
        "_y",
        "_z",
        "Geog",
    ]
    # soup = load_webster_dictionary("_u")
    # web_dict.update(convert_words_from_mw_xml(soup))
    # for letter in alphbat:
    #     soup = load_webster_dictionary(letter)
    #     new_dict = convert_words_from_mw_xml(soup)
    #     web_dict.update(new_dict)
    #     # print(f"new_dict: {new_dict}")
    #     print(f"Finish processing {letter} words.")

    # with open("./vocab/data/mw/mw.word.json", "w") as f:
    #     json.dump(web_dict, f)

    web_dict = load_dictionary("mw")

    # store_examples(cam_dict, "./vocab/data/cambridge/cambridge.examples.txt")
    store_examples(web_dict, "./vocab/data/mw/mw.examples.txt")
