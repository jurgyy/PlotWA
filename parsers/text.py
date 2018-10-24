import datetime
import re
import pandas as pd


MESSAGEDELTA = datetime.timedelta(minutes=5)
CONVERSATIONDELTA = datetime.timedelta(minutes=30)


def get_date(year_match, month_match, day_match):
    day, month, year = int(day_match), int(month_match), int(year_match)
    return datetime.date(2000 + year, month, day)


def get_time(hour_match, minutes_match, h12_match):
    hours, minutes, h12 = int(hour_match), int(minutes_match), str.lower(h12_match)
    if h12[0] == "a" and hours == 12:
        hours = 0
    elif h12[0] == "p" and hours < 12:
        hours += 12

    return datetime.time(hours, minutes)


def parse(fname):
    texts = []
    with open(fname, encoding="utf8") as f:
        content = f.readlines()

        last_timestamp = None
        last_name = ""
        message_id = 0
        conversation_id = 0

        for line in content:
            m = re.search('(\d\d)-(\d\d)-(\d\d),? (\d{1,2}):(\d\d) ([APap]\.?[mM]\.?) - (.*?): (.*)', line)

            if m is None:
                continue

            date = get_date(m.group(3), m.group(2), m.group(1))
            time = get_time(m.group(4), m.group(5), m.group(6))
            name = m.group(7)
            text = m.group(8)
            timestamp = datetime.datetime.combine(date, time)

            if text == "<Media weggelaten>":
                continue

            if last_timestamp is None:
                t_delta = datetime.timedelta(0)
            else:
                t_delta = timestamp - last_timestamp

            if name != last_name or t_delta > MESSAGEDELTA:
                message_id += 1

            if t_delta > CONVERSATIONDELTA:
                conversation_id += 1

            last_timestamp = timestamp
            last_name = name

            texts.append([timestamp, t_delta, message_id - 1, conversation_id, name, text])
    # TODO: name to pd.Categorical data type
    text_dataframe = pd.DataFrame(texts, columns=["datetime", "t_delta", "message_id", "conversation_id", "name", "text"])
    text_dataframe["datetime"] = pd.to_datetime(text_dataframe["datetime"], infer_datetime_format=True)
    text_dataframe.index.name = "text_id"

    return text_dataframe
