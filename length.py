"""
Length
 - Text length distribution
 - Message length distribution (a Message contains of 1 or more consecutive texts from the same person with a gap
                                between them of no larger than 5 minutes)
 - Conversation length by word count, duration and messages
"""

import pandas as pd


def get_length_text(df: pd.DataFrame):
    print("---------text---------")
    num_words_grouper = df.groupby(["name", "num_words"])
    text_length_hist = num_words_grouper["num_words"].agg(["count"])

    length_grouper = df.groupby("name")
    text_length_distr = length_grouper["num_words"].agg(["mean", "std", "count"])

    text_length_hist["normalized"] = text_length_hist["count"].divide(text_length_distr["count"])
    print(text_length_hist)
    print(text_length_distr)


def get_length_message(df: pd.DataFrame):
    pass


def get_length_conversation(df:pd.DataFrame):
    pass


def foo(df: pd.DataFrame):
    get_length_text(df)
