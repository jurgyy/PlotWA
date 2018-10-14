""""
https://i.redd.it/l1l031339vo11.jpg

Goals:
 Activity
 - Activity by calendar day     (https://pythonhosted.org/calmap/)
 - Activity by day of week      (datetime.weekday())
 - Activity by hour of day

 Length
 - Text length distribution
 - Message length distribution (a Message contains of 1 or more consecutive texts from the same person with a gap
                                between them of no larger than 5 minutes)
 - Conversation length by word count, duration and messages

 Emoji/Emoticon     https://stackoverflow.com/questions/43146528/how-to-extract-all-the-emojis-from-text
 - Frequency per emo
 - percent of texts containing one or more emo
 - Most popular emoji per month

 Kisses
 - Kisses by time of day
 - Frequency of number of kisses in a day
 - Kisses over time

 Conversations
 - Distribution of interval between each other
 - Average response time

 Misc
 - "love you" count
 - Word cloud
 - most unique words per person
 - number of texts that contain a question mark
 - number of media files
 - number of urls
"""
import pandas as pd

import length
from parsers import text_parser, kiss_parser, url_parser, emo_parser, sanitizer

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def preprocess(ts):
    emo_stripped, emo_df = emo_parser.parse(ts["text"])
    ts = pd.concat([ts, emo_df], axis=1)
    ts["text"] = emo_stripped

    ts = pd.concat([ts, kiss_parser.parse(ts["text"])], axis=1)

    url_replaced, url_count = url_parser.parse(ts["text"])
    ts = pd.concat([ts, url_count], axis=1)
    ts["text"] = url_replaced

    ts["sanitized"] = sanitizer.parse(ts["text"])

    ts["num_words"] = ts["sanitized"].apply(len)
    return ts


def main():
    # ts = text_parser.parse("data/short.txt")
    ts = text_parser.parse("data/test.txt")
    # ts = text_parser.parse("data/full_conv.txt")
    ts = preprocess(ts)

    print(ts[:10])
    length.foo(ts)


if __name__ == "__main__":
    main()
