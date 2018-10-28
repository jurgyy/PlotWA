import pandas as pd
from collections import Counter
import numpy as np


def most_popular_per_month(df, top_n=3):
    """
    :param df: A parsed and preprocessed texts DataFrame
    :type df: pandas.DataFrame

    :param top_n: The top n most popular emotes that should be returned
    :type top_n: int

    :return: A series object with indices on "name" and "datetime" month with tuples of the most popular emote and the
    frequency
    :rtype: pandas.Series
    """
    tdf = df[["name", "datetime"]].copy()
    tdf.loc[:, "emotes"] = df["emoji"] + df["emoticons"]
    tdf.set_index(pd.DatetimeIndex(tdf["datetime"]), inplace=True)
    interval_grouper = tdf.groupby(["name", pd.Grouper(freq="M")])

    emotes_per_month = interval_grouper["emotes"].sum()
    emotes_per_month[emotes_per_month == tuple()] = np.nan
    emotes_per_month.dropna(inplace=True)

    count_per_month = emotes_per_month.apply(Counter)
    return count_per_month.apply(lambda c: c.most_common(top_n)[0:top_n])


def number_per_message(df):
    """
    :param df: A parsed and preprocessed texts DataFrame
    :type df: pandas.DataFrame

    :return: A series object indexed on "name" with Counter objects of the number of emotes in a message
    :rtype: pandas.Series
    """
    df["emotes"] = df["emoji"] + df["emoticons"]
    message_grouper = df.groupby(["name", "message_id"])
    message_emotes = message_grouper["emotes"].agg("sum")
    num_emotes = message_emotes.apply(lambda s: len(s))
    return num_emotes.groupby("name").apply(list).apply(Counter)


def number_of_emotes(df):
    """
    :param df: A parsed and preprocessed texts DataFrame
    :type df: pandas.DataFrame

    :return: A series object indexed on "name" with Counter objects of how often each emote occurs
    :rtype: pandas.Series
    """
    grouped_emotes = df.groupby("name")["emoji", "emoticons"].agg("sum").apply(lambda s: sum(s, tuple()), axis=1)
    return grouped_emotes.apply(lambda s: Counter(s))


if __name__ == '__main__':
    pass
