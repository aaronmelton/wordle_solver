"""Wordle Solver."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import logging
import sys
from datetime import date
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


def find_green_position(greens_dict, word, green):
    """Build a dictionary of where the green letters are in a word.

    Args
    ----
    word: str
    green: str

    Returns
    -------
    green_position: dict
    """
    logger.debug("START")
    logger.debug("greens_dict=='%s'", greens_dict)
    logger.debug("word=='%s'", word)
    logger.debug("green=='%s'", green)
    for letter in green:
        position = word.find(letter)
        if position == 0:
            greens_dict["column1"] = letter
        if position == 1:
            greens_dict["column2"] = letter
        if position == 2:
            greens_dict["column3"] = letter
        if position == 3:
            greens_dict["column4"] = letter
        if position == 4:
            greens_dict["column5"] = letter
    logger.debug("greens_dict=='%s'", greens_dict)
    logger.debug("STOP")
    return greens_dict


def find_matches(old_dataframe, this_word, track_greens, track_yellows, track_bad_letters):
    """Find matching columns/rows in a Pandas Data Frame.

    Args
    ----
    old_dataframe: pandas.DataFrame()
    this_word: str
    track_greens: str
    track_yellows: str
    track_bad_letters: str

    Returns
    -------
    new_dataframe: pandas.DataFrame()

    """
    logger.debug("START")
    logger.debug("this_word=='%s'", this_word)
    logger.debug("track_greens=='%s'", track_greens)
    logger.debug("track_yellows=='%s'", track_yellows)
    logger.debug("track_bad_letters=='%s'", track_bad_letters)
    new_dataframe = old_dataframe
    # Find all words with green letters in that position.
    if track_greens:
        found_greens = track_greens
        new_dataframe = find_matching_greens(old_dataframe, found_greens)
    # Find all words with yellow letters anywhere in the word.
    if track_yellows:
        new_dataframe = find_matching_yellows(new_dataframe, track_yellows)
    # Remove all words with non-matching letters.
    if track_bad_letters:
        new_dataframe = remove_rows(new_dataframe, track_bad_letters)
    logger.debug("STOP")
    return new_dataframe


def find_matching_greens(this_dataframe, these_columns):
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


def find_matching_yellows(this_dataframe, these_values):
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
        matching_dataframe = matching_dataframe[matching_dataframe.sum(axis=1).str.contains(this_value)]
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
        matching_dataframe = matching_dataframe[matching_dataframe.sum(axis=1).str.contains(this_value) == False]
    logger.debug("STOP")
    return matching_dataframe


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
    word_list = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth"]
    initial_df = build_dataframe(easy_words)

    app_header = f"""{app_dict["name"]} {app_dict["version"]} {app_dict["date"]}"""
    print(app_header)
    print("=" * len(app_header))
    print("")

    for word in word_list:
        this_word = input(f"{word} Word:")
        this_word = this_word.lower()
        if this_word:
            yellow_letters = input("Any Yellows: ")
            yellow_letters = yellow_letters.lower()
            green_letters = input("Any Greens: ")
            green_letters = green_letters.lower()
            print("")

            track_yellows += yellow_letters
            track_yellows = remove_duplicates(track_yellows)
            track_greens += green_letters
            track_greens = remove_duplicates(track_greens)
            track_bad_letters += remove_keep_letters(this_word, yellow_letters + green_letters)
            track_bad_letters = remove_duplicates(track_bad_letters)
            greens_dict = find_green_position(greens_dict, this_word, green_letters)
            matching_df = find_matches(initial_df, this_word, greens_dict, track_yellows, track_bad_letters)

            print(f"""{len(matching_df.sum(axis=1).tolist())} Possible Matches: {matching_df.sum(axis=1).tolist()}""")
            print("")
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
