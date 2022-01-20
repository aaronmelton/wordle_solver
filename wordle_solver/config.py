"""Config file required to support Speedtest Monitor."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os

# Application Variables
app_dict = {
    "author": "Aaron Melton <aaron@aaronmelton.com>",
    "date": "2022-01-20",
    "desc": "A Python script that produces a list of possible words based on results from playing Wordle.",
    "name": "wordle_solver.py",
    "title": "Wordle Solver",
    "url": "https://github.com/aaronmelton/wordle_solver",
    "version": "v0.3.1",
}

# Logging Variables
log_dict = {
    "level": os.environ.get("LOG_LEVEL"),
    "path": os.environ.get("LOG_PATH"),
    "prefix": os.environ.get("LOG_PREFIX"),
}
