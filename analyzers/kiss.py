import pandas as pd
from collections import Counter


def by_hour(df):
    """
    :param df: A parsed and preprocessed texts DataFrame
    :type df: pandas.DataFrame

    :return: A Series with a multiindex on "name" and "hour" with the "num_kisses" that are sent on each "hour"
    :rtype: pandas.Series
    """
    hour_grouper = df.groupby(["name", "hour"])
    return hour_grouper["num_kisses"].agg("sum")


def per_day(df):
    """
    :param df: A parsed and preprocessed texts DataFrame
    :type df: pandas.DataFrame

    :return: A tuple with in the first index a multiindexed DataFrame with index levels "name" and "datetime". The
             DataFrame has two columns: "num_kisses" with the number of kisses on that day and "cumsum" with the total
             number of kisses sent up until that day.
             In the second index of the tuple a Series is returned with a mutliindex with level "name" and "num_kisses".
             In this Series the number of times the "num_kisses" has been sent in a day is stored.
    :rtype: tuple[pandas.DataFrame, pandas.Series]
    """
    # TODO: can perhaps be combined with analyzers.activity.by_day(df)?
    adf = df[["name", "datetime", "num_kisses"]].copy()

    adf.set_index(pd.DatetimeIndex(adf["datetime"]), inplace=True)
    adf.drop("datetime", axis=1, inplace=True)
    day_grouper = adf.groupby(["name", pd.Grouper(freq='D')])
    count_df = day_grouper.agg("sum")

    name_grouper = count_df.groupby("name")
    cumsum = name_grouper.agg("cumsum")
    cumsum.columns = ["cumsum"]
    count_df = pd.concat([count_df, cumsum], axis=1)

    count_series = name_grouper["num_kisses"].apply(Counter)

    return count_df, count_series


if __name__ == '__main__':
    pass