import pandas as pd
import re
import emoji


KISS_EMOJIS = "😘😚😗😙😽💋💏"


def get_x_count(texts: pd.Series):
    return texts.str.count(r"(?<![^ x%s\*])x(?![^ x%s])" % (KISS_EMOJIS, KISS_EMOJIS), re.IGNORECASE)


def get_kiss_emoji_count(texts: pd.Series):
    return texts.str.count(r"[%s]" % KISS_EMOJIS)


def parse(texts: pd.Series):
    s = get_x_count(texts)
    s += get_kiss_emoji_count(texts)
    s.name = "num_kisses"
    return s


if __name__ == '__main__':
    inp =        pd.Series(["word x", "word Xx", "xword", "wordx", "word :x", "*xxx", "x.x", "word 😘😗x word", "😚", "😙", "😽", "x💋", "😚x😚", "x😚x", "💏"])
    expected_x = pd.Series([ 1,        2,         0,       0,       0,         3,      0,     1,                0,    0,    0,   1,     1,      2,      0])
    expected_k = pd.Series([ 0,        0,         0,       0,       0,         0,      0,     2,                1,    1,    1,   1,     2,      1,      1])
    expected =   pd.Series([ 1,        2,         0,       0,       0,         3,      0,     3,                1,    1,    1,   2,     3,      3,      1], name="num_kisses")

    output_x = get_x_count(inp)
    output_k = get_kiss_emoji_count(inp)
    output = parse(inp)

    pd.testing.assert_series_equal(expected_x, output_x)
    pd.testing.assert_series_equal(expected_k, output_k)
    pd.testing.assert_series_equal(expected, output)
