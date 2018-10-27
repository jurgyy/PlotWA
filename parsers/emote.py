import pandas as pd
import emoji


REPLACE_VALUE = "__EMO__"


def get_emojis(texts: pd.Series):
    s = texts.str.findall(emoji.get_emoji_regexp())
    s = s.apply(tuple)
    s.name = "emoji"

    stripped = texts.str.replace(emoji.get_emoji_regexp(), REPLACE_VALUE)
    stripped.name = texts.name

    return stripped, s


def get_emoticons(texts: pd.Series):
    emoticon_pattern = r"[O0]?[\:;\=xX]['\"]?[#\\/\|\)\(O3DoOpPs\]\$]|" \
                       r"\:(?:/+|\(+|\\+|D+)|" \
                       r"[\-^][,\._Ww][\-^]'?|" \
                       r"[\>\<][,\._Ww]?[\>\<]'?|" \
                       r"¯\\_\(ツ\)_/¯|" \
                       r"D+[\:=;]|" \
                       r"\<3"
    s = texts.str.findall(emoticon_pattern)
    s = s.apply(tuple)
    s.name = "emoticons"

    stripped = texts.str.replace(emoticon_pattern, REPLACE_VALUE)
    stripped.name = texts.name

    return stripped, s


def parse(texts: pd.Series):
    texts, emoticons = get_emoticons(texts)
    texts, emojis = get_emojis(texts)
    df = pd.concat([emojis, emoticons], axis=1)
    return texts, df


if __name__ == '__main__':
    emoticon_expected = pd.Series([(":D", ":D"), ("D:",), (">.>",), ("¯\_(ツ)_/¯",), ()], name="emoticons")
    emoticon_replaced, emoticon_result = get_emoticons(
        pd.Series(["xx :D :D", "D:", ">.> xx", "xx ¯\_(ツ)_/¯ xx", "x x"])
    )
    pd.testing.assert_series_equal(emoticon_expected, emoticon_result, check_exact=True)

    emoji_expected = pd.Series([("😃",), ("😃",), ("😃",), ("😃",), ("😃",), ("😃", "😃"), ("😃", "😃"), ()], name="emoji")
    emoji_stripped, emoji_result = get_emojis(
        pd.Series(["😃", "x 😃", "x😃", "x😃x", "😃 x", "x😃x😃x", "x😃😃x", "x x"])
    )
    pd.testing.assert_series_equal(emoji_expected, emoji_result, check_exact=True)

    combined_expected = pd.DataFrame({"emoji": [("😃",), (), ("😃",), (), ("😃", "😃")],
                                      "emoticons": [(":D",), (":D",), (), (), (":D",)]})
    combined_stripped, combined_result = parse(pd.Series(["xx :D😃 xx", "xx :D xx", "xx 😃 xx", "xx xx", "😃:D😃"]))
    pd.testing.assert_frame_equal(combined_expected, combined_result, check_exact=True)

    # TODO: test stripped strings
