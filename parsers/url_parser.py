import pandas as pd
import re


FIND_URL_REGEX = r"((https?|ftp)://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?)"
FIND_DOMAIN_REGEX = r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)"
REPLACE_VALUE = "__URL__"


def parse(texts: pd.Series):
    counts = texts.str.count(FIND_URL_REGEX, flags=re.IGNORECASE)
    counts.name = "url_count"
    replaced = texts.str.replace(FIND_URL_REGEX, REPLACE_VALUE, flags=re.IGNORECASE)
    replaced.name = texts.name

    return replaced, counts


if __name__ == '__main__':
    inp = pd.Series([
        "xx http://xxx.xxx.com/xxx?xx=xx&x=x/ xx http://xxx.xxx.com/xxx?xx=xx&x=x/",
        "http://xxx.xxx.com/xxx?xx=xx&x=x/",
        "http://xxx.xxx.com/xxx?xx=xx&x=x/ xx",
        "xx",
        "xx http://xxx.xxx.com/xxx?xx=xx&x=x/",
    ], name="texts")

    expected_replaced = pd.Series([
        "xx %s xx %s" % (REPLACE_VALUE, REPLACE_VALUE),
        "%s" % REPLACE_VALUE,
        "%s xx" % REPLACE_VALUE,
        "xx",
        "xx %s" % REPLACE_VALUE,
    ], name="texts")

    expected_count = pd.Series([2, 1, 1, 0, 1], name="url_count")
    result_replaced, result_count = parse(inp)

    pd.testing.assert_series_equal(expected_replaced, result_replaced)
    pd.testing.assert_series_equal(expected_count, result_count)
