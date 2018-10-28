import pandas as pd


def by_week_day(df):
    """
    :param df: A parsed and preprocessed texts DataFrame
    :type df: pandas.DataFrame

    :return: A series object with indices on "name" and "weekday" with the total number of texts sent on that weekday
    where Monday=0 and Sunday=6.
    :rtype: pandas.Series
    """
    day_grouper = df.groupby(["name", "weekday"])
    return day_grouper["weekday"].agg("count")


def by_hour(df):
    """
    :param df: A parsed and preprocessed texts DataFrame
    :type df: pandas.DataFrame

    :return: A series object with indices on "name" and "hour" with the total number of texts sent in that hour where
    12 a.m. = 0 and 11 p.m. is 23.
    :rtype: pandas.Series
    """
    hour_grouper = df.groupby(["name", "hour"])
    return hour_grouper["hour"].agg("count")


def by_day(df):
    """
    :param df: A parsed and preprocessed texts DataFrame
    :type df: pandas.DataFrame

    :return: A series object with indices on "name" and "date" with the total number of texts sent on that date where.
    :rtype: pandas.Series
    """
    adf = df[["name", "datetime"]].copy()

    adf.set_index(pd.DatetimeIndex(adf["datetime"]), inplace=True)
    day_grouper = adf.groupby(["name", pd.Grouper(freq='D')])
    count_df = day_grouper.agg("count")["datetime"]
    count_df.index.names = ["name", "date"]
    return count_df


if __name__ == '__main__':
    pass
