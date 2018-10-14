import pandas as pd
import unicodedata


def strip_accents(texts: pd.Series):
    """
    :param texts:
    :type texts: pd.Series.

    :returns: The processed Series.
    :rtype: pd.Series.
    """
    # try:
    #     text = str(text, 'utf-8')
    # except (TypeError, NameError):  # unicode is a default on python 3
    #     pass

    texts = texts.apply(lambda t: unicodedata.normalize('NFD', t))
    texts = texts.str.encode('ascii', 'ignore')
    texts = texts.str.decode("utf-8")
    return texts


def to_lower(texts: pd.Series):
    return texts.str.lower()


def strip_punctuation_and_whitespace(texts: pd.Series):
    texts = texts.str.replace(r"\s*[^\w\s]+\s*", " ")
    return texts.str.strip()


def strip_repeated_letters(texts: pd.Series):
    return texts.str.replace(r"([a-z])\1+", r"\1\1")


def strip_single_letters(texts: pd.Series):
    return texts.str.replace(r"\b[a-z]\s\b|\b\s[a-z]\b|\b[a-z]\b", "")


def parse(texts: pd.Series):
    sanitized = strip_repeated_letters(
        strip_single_letters(
            strip_punctuation_and_whitespace(
                to_lower(
                    strip_accents(texts)
                )
            )
        )
    )
    sanitized.name = "sanitized"
    return sanitized.str.split(' ')


if __name__ == '__main__':
    inp_accents = pd.Series(["éáúóíëäüöïèàùòìõã"])
    expected_accents = pd.Series(["eauoieauoieauoioa"])
    pd.testing.assert_series_equal(expected_accents, strip_accents(inp_accents))

    inp_lower = pd.Series(["ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz"])
    expected_lower = pd.Series(["abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz"])
    pd.testing.assert_series_equal(expected_lower, to_lower(inp_lower))

    inp_punct = pd.Series(["!xx!", "xx, xx", "xx...xx", " xx: xx "])
    expected_punct = pd.Series(["xx", "xx xx", "xx xx", "xx xx"])
    pd.testing.assert_series_equal(expected_punct, strip_punctuation_and_whitespace(inp_punct))
    
    inp_single = pd.Series(["xx", "x", "xx x", "x xx", "x x", "x x x", "x xx x", "xx xx xx", "1 xx 1", "x 1x x"])
    expected_single = pd.Series(["xx", "", "xx", "xx", "", "", "xx", "xx xx xx", "1 xx 1", "1x"])
    pd.testing.assert_series_equal(expected_single, strip_single_letters(inp_single))
    
    inp_repeat = pd.Series(["xy", "xxyy", "xxxyyyyy", "xxxyy", "xyxy", "xyyyx", "xxx yyyyy xxx"])
    expected_repeat = pd.Series(["xy", "xxyy", "xxyy", "xxyy", "xyxy", "xyyx", "xx yy xx"])
    pd.testing.assert_series_equal(expected_repeat, strip_repeated_letters(inp_repeat))

    inp_combined = pd.Series(["Äá!", "ÈË, õÕ, 111", "éË...XX", " Xx: xX ", "à éì õ"])
    expected_combined = pd.Series([["aa"], ["ee", "oo", "111"], ["ee", "xx"], ["xx", "xx"], ["ei"]], name="sanitized")
    pd.testing.assert_series_equal(expected_combined, parse(inp_combined))

