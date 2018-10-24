"""
 Emoji/Emoticon     https://stackoverflow.com/questions/43146528/how-to-extract-all-the-emojis-from-text
 - Frequency per emote
 - percent of messages containing emotes and how much
 - Most popular emoji per month
"""
# TODO: per person or combined?

import pandas as pd
from collections import Counter
import numpy as np
import sys


def most_popular(df: pd.DataFrame, top_n: int, per="month"):
    pass
    tdf = df[["datetime"]]
    tdf["emotes"] = df["emoji"] + df["emoticons"]

    tdf.set_index(pd.DatetimeIndex(tdf["datetime"]), inplace=True)
    interval_grouper = tdf.groupby(pd.Grouper(freq="M"))
    print(tdf)


def number_per_message(df: pd.DataFrame):
    """
    :param df: A parsed and preprocessed texts DataFrame
    :type: pandas.DataFrame

    :return: Counter object of the number of number of emotes in a message
    :rtype: collections.Counter
    """
    message_grouper = df.groupby("message_id")
    message_emotes = message_grouper["emoji", "emoticons"].agg("sum")
    return Counter((message_emotes["emoji"] + message_emotes["emoticons"]).apply(lambda s: len(s)))


def number_of_emotes(df: pd.DataFrame):
    """
    :param df: A parsed and preprocessed texts DataFrame
    :type: pandas.DataFrame

    :return: Counter object with how often each emote occurs
    :rtype: collections.Counter
    """
    return Counter(df["emoji"].sum() + df["emoticons"].sum())


def foo(df: pd.DataFrame):
    number_of_emotes(df)
    number_per_message(df)
    most_popular(df, 1, per="month")


if __name__ == '__main__':
    pass
