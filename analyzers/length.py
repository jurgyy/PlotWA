import pandas as pd
from collections import Counter


def get_length_text(df):
    """
    :param df: A parsed and preprocessed texts DataFrame
    :type df: pandas.DataFrame

    :return: A tuple with in the first index a multiindexed DataFrame with index levels "name" and "num_words". The
             DataFrame has two columns: "count" with the number of times a text with "num_words" occurred and
             "normalized" with count normalized so that for each "name" the values add up to one.
             In the second index of the tuple a distribution DataFrame is returned. This DataFrame is indexed by "name"
             and has columns "mean" with the mean of the number of words, "std" with the standard deviation and "count"
             with the total number of words.
    :rtype: tuple[Pandas.DataFrame]
    """
    num_words_grouper = df.groupby(["name", "num_words"])
    text_length_hist = num_words_grouper["num_words"].agg(["count"])

    length_grouper = df.groupby("name")
    text_length_distr = length_grouper["num_words"].agg(["mean", "std", "count"])

    text_length_hist["normalized"] = text_length_hist["count"].divide(text_length_distr["count"])
    return text_length_hist, text_length_distr


def get_length_message(df):
    """
    :param df: A parsed and preprocessed texts DataFrame
    :type df: pandas.DataFrame

    :return: A tuple with in the first index a multiindexed DataFrame with index levels "name" and "message_id". The
             DataFrame has three columns: "num_words" with the number of words in a message, "num_texts" with the number
             of texts in a message and "normalized" with the normalized number of words so that for each "name" the
             values add up to one.
             In the second index of the tuple a distribution DataFrame is returned. This DataFrame is indexed by "name"
             and has columns "mean" with the mean of the number of words, "std" with the standard deviation and "count"
             with the total number of words.
    :rtype: tuple[pandas.DataFrame]
    """
    num_words_grouper = df.groupby(["name", "message_id"])
    text_length_hist = num_words_grouper["num_words"].agg(["sum", "count"])
    text_length_hist.columns = ["num_words", "num_texts"]

    length_grouper = df.groupby("name")
    text_length_distr = length_grouper["num_words"].agg(["mean", "std", "sum"])

    text_length_hist["normalized"] = text_length_hist["num_words"].divide(text_length_distr["sum"])
    return text_length_hist, text_length_distr


def get_length_conversation(df):
    """
    :param df: A parsed and preprocessed texts DataFrame
    :type df: pandas.DataFrame

    :return: A multi indexed DataFrame with index levels conversation_id and name. The DataFrame has mulitlevel columns
             namely:
              "name" with "count" that contains the number of texts per person.
              "num_words" with "sum", this contains the total number of words per person.
              "message_id" with "nunique" which contains the number of messages per person.
              "timestamp" with "min" and "max" which are the first and last timestamps of the conversation per person.
    :rtype: pandas.DataFrame
    """
    conv_grouper = df.groupby(["conversation_id", "name"])
    convs = conv_grouper["name", "num_words", "message_id", "datetime"].agg({
        "name": ["count"],
        "num_words": ["sum"],
        "message_id": [pd.Series.nunique],
        "datetime": ["min", "max"]
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
