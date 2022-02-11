"""Wordle Solver."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import logging
import sys
from datetime import date
from string import ascii_lowercase

import pandas
from config import app_dict, log_dict
from wordle_words import easy_words, hard_words


class WordleDataFrame:
    """Object for all possible solutions to Wordle."""

    def __init__(self, this_list):
        """Build a Pandas DataFrame using a Python List.

        Args
        ----
        self: pandas.DataFrame
        this_list: list

        Returns
        -------
        self.frame: pandas.DataFrame
        """
        logger.debug("START")
        column1 = []
        column2 = []
        column3 = []
        column4 = []
        column5 = []
        value = []
        word_dict = {}

        for this_word in this_list:
            column1 += this_word[0]
            column2 += this_word[1]
            column3 += this_word[2]
            column4 += this_word[3]
            column5 += this_word[4]
            value = 0

        word_dict = {
            "column1": column1,
            "column2": column2,
            "column3": column3,
            "column4": column4,
            "column5": column5,
            "value": value,
        }
        logger.debug("STOP")
        self.frame = pandas.DataFrame(word_dict).drop_duplicates()

    def find_matching_columns(self, this_word):
        """Find matching columns.

        Args
        ----
        self: pandas.DataFrame
        this_word: list

        Returns
        -------
        self.frame: pandas.DataFrame
        """
        logger.debug("START")
        logger.debug("this_word=='%s'")
        if this_word[0] != " ":
            self.frame = self.frame.loc[self.frame["column1"] == this_word[0]]
        if this_word[1] != " ":
            self.frame = self.frame.loc[self.frame["column2"] == this_word[1]]
        if this_word[2] != " ":
            self.frame = self.frame.loc[self.frame["column3"] == this_word[2]]
        if this_word[3] != " ":
            self.frame = self.frame.loc[self.frame["column4"] == this_word[3]]
        if this_word[4] != " ":
            self.frame = self.frame.loc[self.frame["column5"] == this_word[4]]
        logger.debug("STOP")

    def del_nonmatching_columns(self, this_word):
        """Remove non-matching columns.

        Args
        ----
        self: pandas.DataFrame
        this_word: list

        Returns
        -------
        self.frame: pandas.DataFrame
        """
        logger.debug("START")
        logger.debug("this_word=='%s'", this_word)
        if this_word[0] != " ":
            self.frame = self.frame.loc[self.frame["column1"] != this_word[0]]
        if this_word[1] != " ":
            self.frame = self.frame.loc[self.frame["column2"] != this_word[1]]
        if this_word[2] != " ":
            self.frame = self.frame.loc[self.frame["column3"] != this_word[2]]
        if this_word[3] != " ":
            self.frame = self.frame.loc[self.frame["column4"] != this_word[3]]
        if this_word[4] != " ":
            self.frame = self.frame.loc[self.frame["column5"] != this_word[4]]
        logger.debug("STOP")

    def del_matching_rows(self, these_letters):
        """Remove matching rows.

        Args
        ----
        self: pandas.DataFrame
        these_letters: str

        Returns
        -------
        self.frame: pandas.DataFrame
        """
        logger.debug("START")
        logger.debug("these_letters=='%s'", these_letters)
        column_list = ["column1", "column2", "column3", "column4", "column5"]
        for letter in these_letters:
            self.frame = self.frame[self.frame[column_list].sum(axis=1).astype(str).str.contains(letter) == False]
        logger.debug("STOP")

    def del_nonmatching_rows(self, these_letters):
        """Remove non-matching rows.

        Args
        ----
        self: pandas.DataFrame
        these_letters: str

        Returns
        -------
        self.frame: pandas.DataFrame
        """
        logger.debug("START")
        logger.debug("these_letters=='%s'", these_letters)
        column_list = ["column1", "column2", "column3", "column4", "column5"]
        for letter in these_letters:
            self.frame = self.frame[self.frame[column_list].sum(axis=1).astype(str).str.contains(letter) == True]
        logger.debug("STOP")


def find_no_matches(guess, greens, yellows):
    """Find gray letters so we can remove all rows that contain them.

    Args
    ----
    guess: str
    greens: str
    yellows: str

    Returns
    -------
    : str
    """
    logger.debug("START")
    logger.debug("guess=='%s'", guess)
    logger.debug("greens=='%s'", greens)
    logger.debug("yellows=='%s'", yellows)
    del_this = []
    guess = list(guess)
    greens = list(greens)
    yellows = list(yellows)
    for _, letter in enumerate(guess):
        if not (letter in greens) and not (letter in yellows):
            del_this.append(letter)
    logger.debug("del_this=='%s'", del_this)
    logger.debug("STOP")
    return "".join(del_this)


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
        validated_input = validated_input.lower()
        validated = validate_input(validated_input)
    logger.debug("validated_input==%s", validated_input)
    logger.debug("STOP")
    return validated_input


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
    logger.debug("input_string=='%s'", input_string)
    valid = False
    # Accept ENTER (no string) as valid input
    if input_string == "":
        valid = True
    # Only 5-character words are valid
    elif len(input_string) != 5:
        valid = False
    else:
        # Only valid string are ASCII characters
        for letter in input_string:
            if letter in ascii_lowercase:
                valid = True
            elif letter == " ":
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

    logger.info("START START START")
    logger.info(
        "%s %s (%s)",
        app_dict["name"],
        app_dict["version"],
        app_dict["date"],
    )

    logger.debug("""app_dict["difficulty"]=='%s'""", app_dict["difficulty"])
    if app_dict["difficulty"] == "hard":
        logger.info("Using easy and hard words...")
        these_words = set(easy_words + hard_words)
    else:
        logger.info("Using easy words...")
        these_words = easy_words

    logger.info("Loading %s words from word file...", len(these_words))

    app_header = f"""{app_dict["name"]} {app_dict["version"]} {app_dict["date"]}"""
    print(app_header)
    print("=" * len(app_header))
    print("")
    print("INSTRUCTIONS:")
    print("Guess your 5-letter word.")
    print(
        "Enter any matching green/yellow letters using a space as a placeholder for non-matching letters in the word."
    )
    print("")
    print("EXAMPLE:")
    print("First Word:  crane\nAny Greens:      e\nAny Yellows:   a  ")
    print("")

    wdf = WordleDataFrame(these_words)

    for word in ["First", "Second", "Third", "Fourth", "Fifth", "Sixth"]:
        this_word = get_input(f"{word} Word: ".rjust(13, " "))
        logger.info("User guessed word: '%s'", this_word)
        if this_word:
            green_letters = get_input("Any Greens: ".rjust(13, " "))
            yellow_letters = get_input("Any Yellows: ".rjust(13, " "))
            if green_letters:
                logger.info("Processing Green Letters...")
                wdf.find_matching_columns(green_letters)
            if yellow_letters:
                logger.info("Processing Yellow Letters...")
                wdf.del_nonmatching_columns(yellow_letters)
            wdf.del_matching_rows(find_no_matches(this_word, green_letters, yellow_letters))
            wdf.del_nonmatching_rows(yellow_letters.replace(" ", ""))

            print("")
            print(f"{len(wdf.frame)} possible matches...")
            column_list = ["column1", "column2", "column3", "column4", "column5"]
            print(wdf.frame.sort_values(by=column_list)[column_list].sum(axis=1).tolist())
            print("")
            if len(wdf.frame) <= 2:
                break
        # Quit if no input
        elif not this_word:
            break

    logger.info("STOP STOP STOP")
    return 0


if __name__ == "__main__":
    pandas.set_option("display.max_rows", None)
    logger = logging.getLogger(__name__)
    sys.exit(main())
