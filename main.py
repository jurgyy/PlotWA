""""
https://i.redd.it/l1l031339vo11.jpg

Goals:
 Lists indicate:
   [P, A, I, U] Objective description
   P: Parse - Data is available in an easy to use format
   A: Analyze - Data is processed and reduced to a single-use format
   I: Image - The data can be transformed in an image
   U: UI - The objective can be selected from a UI

 Ticks indicate:
   _: Not started yet
   W: Work in progress
   X: Not feasible
   N: Not Applicable

 Activity
 [✓, ✓, _, _] Activity by calendar day     (https://pythonhosted.org/calmap/)
 [✓, ✓, _, _] Activity by day of week      (datetime.weekday())
 [✓, ✓, _, _] Activity by hour of day

 Length
 [✓, ✓, _, _] Text length distribution
 [✓, ✓, _, _] Message length distribution (a Message contains of 1 or more consecutive texts from the same person with
               a gap between them of no larger than 5 minutes)
 [✓, ✓, _, _] Conversation length by word count, duration and messages

 Emoji/Emoticon     https://stackoverflow.com/questions/43146528/how-to-extract-all-the-emojis-from-text
 [✓, ✓, _, _] Frequency per emo
 [✓, ✓, _, _] percent of texts containing one or more emo
 [✓, ✓, _, _] Most popular emoji per month

 Kisses
 [✓, ✓, _, _] Kisses by time of day
 [✓, ✓, _, _] Frequency of number of kisses in a day
 [✓, ✓, _, _] Kisses over time

 Conversations
 [✓, ✓, _, _] Distribution of interval between each other
 [✓, ✓, _, _] Average response time within a conversation
 [✓, ✓, _, _] Longest time between two texts of each other


 Word Semantics and Corpus statistics
 [_, _, _, _] Word Cloud
 [_, _, _, _] Top-K TF-IDF (most unique words per person)
 [_, _, _, _] Total number of words
 [_, _, _, _] Unique words

 Misc
 [_, _, _, _] "love you" count
 [_, _, _, _] number of texts that contain a question mark
 [_, _, _, _] number of media files
 [_, _, _, _] number of urls

 Other:
    Optimize: https://engineering.upside.com/a-beginners-guide-to-optimizing-pandas-code-for-speed-c09ef2c6a4d6
"""
import pandas as pd
from flask import Flask, redirect, request, render_template
from flask import flash as fflash

import analyzers
import parsers

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

app = Flask(__name__)


def flash(*arg, **kwargs):
    print(*arg, **kwargs)
    fflash(*arg, **kwargs)


@app.route("/")
def homepage():
    return render_template("main.html")


@app.route("/", methods=["POST"])
def main_post():
    if 'textfile' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files["textfile"].read()
    return str(file).replace("<Media weggelaten>", "[media]").replace("\\r\\n", "<br>").replace("\\n", "<br>")


def preprocess(ts):
    emo_stripped, emo_df = parsers.emote.parse(ts["text"])
    ts = pd.concat([ts, emo_df], axis=1)
    ts["text"] = emo_stripped

    ts = pd.concat([ts, parsers.kiss.parse(ts["text"])], axis=1)

    url_replaced, url_count = parsers.url.parse(ts["text"])
    ts = pd.concat([ts, url_count], axis=1)
    ts["text"] = url_replaced

    ts["sanitized"] = parsers.sanitizer.parse(ts["text"])

    ts["num_words"] = ts["sanitized"].apply(len)
    return ts


def main():
    app.secret_key = "0"
    app.run()
    # ts = text.parse("data/short.txt")
    # ts = parsers.text.parse("data/test.txt")
    # ts = text.parse("data/full_conv.txt")
    # ts = preprocess(ts)

    # print(ts[:25])
    # print(analyzers.activity.by_hour(ts))
    # print(analyzers.activity.by_week_day(ts))
    # print(analyzers.activity.by_day(ts))
    # length.foo(ts)
    # emote_analyzer.foo(ts)
    # print(analyzers.length.get_length_conversation(ts))
    # print(analyzers.conv.conversation_interval_distribution(ts))


if __name__ == "__main__":
    main()
