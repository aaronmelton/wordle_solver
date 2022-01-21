"""Wordle Solver."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import logging
import sys
from datetime import date
from string import ascii_lowercase
from time import time

import pandas
from config import app_dict, log_dict
from wordle_words import easy_words


def build_dataframe(this_list):
    """Build a Pandas DataFrame using a Python List.

    Args
    ----
    this_list: list

    Returns
    -------
    dataframe: pandas.DataFrame()
    """
    logger.debug("START")
    column1 = []
    column2 = []
    column3 = []
    column4 = []
    column5 = []
    word_dict = {}

    for this_word in this_list:
        column1 += this_word[0]
        column2 += this_word[1]
        column3 += this_word[2]
        column4 += this_word[3]
        column5 += this_word[4]

    word_dict = {
        "column1": column1,
        "column2": column2,
        "column3": column3,
        "column4": column4,
        "column5": column5,
    }
    logger.debug("STOP")
    return pandas.DataFrame(word_dict)


def find_letter_position(words_dict, word, letters):
    """Build a dictionary of where the letters are in a word.

    Args
    ----
    words_dict: dict
    word: str
    letters: str

    Returns
    -------
    words_dict: dict
    """
    logger.debug("START")
    logger.debug("words_dict=='%s'", words_dict)
    logger.debug("word=='%s'", word)
    logger.debug("letters=='%s'", letters)
    for letter in letters:
        position = word.find(letter)
        if position == 0:
            words_dict["column1"] = letter
        if position == 1:
            words_dict["column2"] = letter
        if position == 2:
            words_dict["column3"] = letter
        if position == 3:
            words_dict["column4"] = letter
        if position == 4:
            words_dict["column5"] = letter
    logger.debug("words_dict=='%s'", words_dict)
    logger.debug("STOP")
    return words_dict


def find_matches(**kwargs):
    """Find matching columns/rows in a Pandas Data Frame.

    Args
    ----
    old_dataframe: pandas.DataFrame()
    this_word: str
    track_greens: str
    yellows_dict: dict
    track_yellows: str
    track_bad_letters: str

    Returns
    -------
    new_dataframe: pandas.DataFrame()

    """
    logger.debug("START")
    old_dataframe = kwargs["initial_df"]
    this_word = kwargs["this_word"]
    track_greens = kwargs["track_greens"]
    yellows_dict = kwargs["yellows_dict"]
    track_yellows = kwargs["track_yellows"]
    track_bad_letters = kwargs["track_bad_letters"]
    logger.debug("this_word=='%s'", this_word)
    logger.debug("track_greens=='%s'", track_greens)
    logger.debug("yellows_dict=='%s'", yellows_dict)
    logger.debug("track_yellows=='%s'", track_yellows)
    logger.debug("track_bad_letters=='%s'", track_bad_letters)
    new_dataframe = old_dataframe
    # Find all words with green letters in that position.
    if track_greens:
        new_dataframe = find_matching_columns(old_dataframe, track_greens)
    # Find all words with yellow letters anywhere in the word.
    if track_yellows:
        new_dataframe = find_matching_rows(new_dataframe, track_yellows)
        new_dataframe = remove_columns(new_dataframe, yellows_dict)
    # Remove all words with non-matching letters.
    if track_bad_letters:
        new_dataframe = remove_rows(new_dataframe, track_bad_letters)
    logger.debug("STOP")
    return new_dataframe


def find_matching_columns(this_dataframe, these_columns):
    """Find matching columns in a Pandas Data Frame.  We know the green letters \
    positions so we will search columns for those letters.

    Args
    ----
    this_dataframe: pandas.DataFrame()
    these_columns: dict

    Returns
    -------
    matching_dataframe: pandas.DataFrame()
    """
    logger.debug("START")
    logger.debug("these_columns=='%s'", these_columns)
    matching_dataframe = this_dataframe
    if these_columns["column1"]:
        matching_dataframe = matching_dataframe.loc[(matching_dataframe["column1"] == these_columns["column1"])]
    if these_columns["column2"]:
        matching_dataframe = matching_dataframe.loc[(matching_dataframe["column2"] == these_columns["column2"])]
    if these_columns["column3"]:
        matching_dataframe = matching_dataframe.loc[(matching_dataframe["column3"] == these_columns["column3"])]
    if these_columns["column4"]:
        matching_dataframe = matching_dataframe.loc[(matching_dataframe["column4"] == these_columns["column4"])]
    if these_columns["column5"]:
        matching_dataframe = matching_dataframe.loc[(matching_dataframe["column5"] == these_columns["column5"])]
    logger.debug("STOP")
    return matching_dataframe


def find_matching_rows(this_dataframe, these_values):
    """Find matching rows in a Pandas Data Frame.  We don't know the yellow \
    letters position so we will search rows for those letters.

    Args
    ----
    this_dataframe: pandas.DataFrame()
    these_value: str

    Returns
    -------
    matching_dataframe: pandas.DataFrame()
    """
    logger.debug("START")
    logger.debug("these_values=='%s'", these_values)
    matching_dataframe = this_dataframe
    for this_value in these_values:
        matching_dataframe = matching_dataframe[matching_dataframe.sum(axis=1).astype(str).str.contains(this_value)]
    logger.debug("STOP")
    return matching_dataframe


def get_input(message):
    """Get input from the User and then validate input.

    Args
    ----
    message: str
    input_string: str

    Returns
    -------
    validated_input: str

    """
    logger.debug("START")
    logger.debug("message==%s", message)
    validated_input = ""
    validated = False
    while not validated:
        validated_input = input(message)
        validated_input = validated_input.strip().lower()
        validated = validate_input(validated_input)
    logger.debug("validated_input==%s", validated_input)
    logger.debug("STOP")
    return validated_input


def remove_columns(this_dataframe, these_columns):
    """Find and remove matching columns in a Pandas Data Frame.  We know the \
    yellow letters positions and they were not matches so we will search \
    columns for those letters and remove them from potential matches.

    Args
    ----
    this_dataframe: pandas.DataFrame()
    these_columns: dict

    Returns
    -------
    matching_dataframe: pandas.DataFrame()
    """
    logger.debug("START")
    logger.debug("these_columns=='%s'", these_columns)
    matching_dataframe = this_dataframe
    if these_columns["column1"]:
        matching_dataframe = matching_dataframe.loc[(matching_dataframe["column1"] != these_columns["column1"])]
    if these_columns["column2"]:
        matching_dataframe = matching_dataframe.loc[(matching_dataframe["column2"] != these_columns["column2"])]
    if these_columns["column3"]:
        matching_dataframe = matching_dataframe.loc[(matching_dataframe["column3"] != these_columns["column3"])]
    if these_columns["column4"]:
        matching_dataframe = matching_dataframe.loc[(matching_dataframe["column4"] != these_columns["column4"])]
    if these_columns["column5"]:
        matching_dataframe = matching_dataframe.loc[(matching_dataframe["column5"] != these_columns["column5"])]
    logger.debug("STOP")
    return matching_dataframe


def remove_duplicates(word):
    """Remove duplicate letters from a string.

    Args
    ----
    word: str

    Returns
    -------
    new_word: str
    """
    logger.debug("START")
    logger.debug("word=='%s'", word)
    new_word = set(word)
    new_word = "".join(new_word)
    logger.debug("new_word=='%s'", new_word)
    logger.debug("STOP")
    return new_word


def remove_keep_letters(word, keep_letters):
    """Build a list of non-matching letters.

    Args
    ----
    word: str
    letters: str

    Returns
    -------
    bad_letters: str
    """
    logger.debug("START")
    logger.debug("word=='%s'", word)
    logger.debug("keep_letters=='%s'", keep_letters)
    bad_letters = ""
    for letter in word:
        if letter not in keep_letters:
            bad_letters += letter
            word = word.replace(letter, "")
    logger.debug("bad_letters=='%s'", bad_letters)
    logger.debug("STOP")
    return bad_letters


def remove_rows(this_dataframe, these_values):
    """Remove rows in a Panda Data Frame that aren't matches.

    Args
    ----
    this_dataframe: pandas.DataFrame()
    these_value: str

    Returns
    -------
    matching_dataframe: pandas.DataFrame()
    """
    logger.debug("START")
    logger.debug("these_values=='%s'", these_values)
    matching_dataframe = this_dataframe
    for this_value in these_values:
        matching_dataframe = matching_dataframe[
            matching_dataframe.sum(axis=1).astype(str).str.contains(this_value) == False
        ]
    logger.debug("STOP")
    return matching_dataframe


def validate_input(input_string):
    """Validate input provided by the User.

    Args
    ----
    input_string: str

    Returns
    -------
    valid: bool

    """
    logger.debug("START")
    logger.debug("input_string==%s", input_string)
    valid = False
    # Accept ENTER (no string) as valid input
    if input_string == "":
        valid = True
    else:
        # Only valid string are ASCII characters
        for letter in input_string:
            if letter in ascii_lowercase:
                valid = True
            else:
                valid = False
                break
    logger.debug("valid==%s", valid)
    logger.debug("STOP")
    return valid


def main():
    """Main Function.

    Args
    ----
    None

    Returns
    -------
    None
    """
    start_time = time()

    # Setup Logging Functionality
    logging.basicConfig(
        # pylint: disable=line-too-long
        filename=f"""{log_dict["path"]}{log_dict["prefix"]}{date.today().strftime("%Y%m%d")}.log""",
        filemode="a",
        format="{asctime}  Log Level: {levelname:8}  Line: {lineno:4}  Function: {funcName:21}  Msg: {message}",
        style="{",
        datefmt="%Y-%m-%dT%H:%M:%S",
        level=log_dict["level"],
    )

    logger.info("")
    logger.info("")
    logger.info("")
    logger.info("START START START")
    logger.info(
        "%s %s (%s)",
        app_dict["name"],
        app_dict["version"],
        app_dict["date"],
    )

    track_yellows = ""
    track_greens = ""
    track_bad_letters = ""
    greens_dict = {
        "column1": None,
        "column2": None,
        "column3": None,
        "column4": None,
        "column5": None,
    }
    yellows_dict = {
        "column1": None,
        "column2": None,
        "column3": None,
        "column4": None,
        "column5": None,
    }
    word_list = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth"]
    initial_df = build_dataframe(easy_words)

    app_header = f"""{app_dict["name"]} {app_dict["version"]} {app_dict["date"]}"""
    print(app_header)
    print("=" * len(app_header))
    print("")

    for word in word_list:
        this_word = get_input(f"{word} Word: ")
        if this_word:
            yellow_letters = get_input("Any Yellows: ")
            green_letters = get_input("Any Greens: ")
            print("")

            track_yellows += yellow_letters
            track_yellows = remove_duplicates(track_yellows)
            track_greens += green_letters
            track_greens = remove_duplicates(track_greens)
            track_bad_letters += remove_keep_letters(this_word, yellow_letters + green_letters)
            track_bad_letters = remove_duplicates(track_bad_letters)
            greens_dict = find_letter_position(greens_dict, this_word, green_letters)
            yellows_dict = find_letter_position(yellows_dict, this_word, yellow_letters)
            matching_df = find_matches(
                initial_df=initial_df,
                this_word=this_word,
                track_greens=greens_dict,
                yellows_dict=yellows_dict,
                track_yellows=track_yellows,
                track_bad_letters=track_bad_letters,
            )

            print(f"""{len(matching_df.sum(axis=1).tolist())} Possible Match(es): {matching_df.sum(axis=1).tolist()}""")
            print("")
            # If only one solution is provided, quit.
            if len(matching_df.sum(axis=1).tolist()) == 1:
                break
        elif not this_word:
            break

    logger.info("Total Execution Time: %s seconds", time() - start_time)
    logger.info("STOP STOP STOP")
    return 0


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    sys.exit(main())
