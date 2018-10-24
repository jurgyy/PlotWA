"""
Length
 - Text length distribution
 - Message length distribution (a Message contains of 1 or more consecutive texts from the same person with a gap
                                between them of no larger than 5 minutes)
 - Conversation length by word count, duration and messages
"""

"""
6                          
5       aa     bb          
4  aa   aa   aabb          
3  aabb aabb aabb          
2  aabb aabb aabb    bb     
1  aabb aabb aabb    bb     
    0    1    2     3    
"""


import pandas as pd
from collections import Counter


def get_length_text(df: pd.DataFrame):
    num_words_grouper = df.groupby(["name", "num_words"])
    text_length_hist = num_words_grouper["num_words"].agg(["count"])

    length_grouper = df.groupby("name")
    text_length_distr = length_grouper["num_words"].agg(["mean", "std", "count"])

    text_length_hist["normalized"] = text_length_hist["count"].divide(text_length_distr["count"])
    return text_length_hist, text_length_distr


def get_length_message(df: pd.DataFrame):
    num_words_grouper = df.groupby(["name", "message_id"])
    text_length_hist = num_words_grouper["num_words"].agg(["sum", "count"])
    text_length_hist.columns = ["num_words", "num_texts"]

    length_grouper = df.groupby("name")
    text_length_distr = length_grouper["num_words"].agg(["mean", "std", "sum"])

    text_length_hist["normalized"] = text_length_hist["num_words"].divide(text_length_distr["sum"])
    return text_length_hist, text_length_distr


def get_length_conversation(df: pd.DataFrame):
    """
    :param df: A parsed and preprocessed texts DataFrame
    :type: pandas.DataFrame

    :return: A multi indexed DataFrame with index levels conversation_id and name. The DataFrame has mulitlevel columns
             namely:
              "name" with "count" that contains the number of texts per person.
              "num_words" with "sum", this contains the total number of words per person.
              "message_id" with "nunique" which contains the number of messages per person.
              "timestamp" with "min" and "max" which are the first and last timestamps of the conversation per person.
    :rtype: pandas.DataFrame
    """
    conv_grouper = df.groupby(["conversation_id", "name"])
    convs = conv_grouper["name", "num_words", "message_id", "timestamp"].agg({
        "name": ["count"],
        "num_words": ["sum"],
        "message_id": [pd.Series.nunique],
        "timestamp": ["min", "max"]
    })

    conv_length = pd.DataFrame.from_dict(Counter(convs.index.labels[0]), orient="index")[0]
    convs.drop(conv_length.index[conv_length == 1], inplace=True)
    return convs


def foo(df: pd.DataFrame):
    a, b = get_length_text(df)
    print(a)
    print(b)
    print("----")
    a, b = get_length_message(df)
    print(a)
    print(b)
    print("----")
    a = get_length_conversation(df)
    print(a)


if __name__ == '__main__':
    # TODO: unit tests
    pass
