def response_time_distribution(df):
    """
    :param df: A parsed and preprocessed texts DataFrame
    :type df: pandas.DataFrame

    :return: A DataFrame indexed on 'name' with the 'count', 'mean', standard deviation ('std'), 'min', lower '25%',
             '50%', '75%' and 'max' value of the in-conversation response time.
    :rtype: pandas.DataFrame
    """
    shift = df.shift()
    is_reply = (df["name"] != shift["name"]) & (df["conversation_id"] == shift["conversation_id"])
    return df[is_reply].groupby(df["name"])["t_delta"].describe()


def conversation_interval_distribution(df):
    """
    :param df: A parsed and preprocessed texts DataFrame
    :type df: pandas.DataFrame

    :return: A Series with the 'count', 'mean', standard deviation ('std'), 'min', lower '25%', '50%', '75%' and 'max'
             value of the time between conversations.
    :rtype: pandas.Series
    """
    shift = df["name"].shift()
    shift.iloc[0] = df["name"].iloc[0]
    speaker_switched = df["name"] != shift

    # noinspection PyUnresolvedReferences
    consecutive_speaker_id = speaker_switched.cumsum()
    return df.groupby(consecutive_speaker_id.drop(0))["t_delta"].first().describe()


if __name__ == '__main__':
    pass
