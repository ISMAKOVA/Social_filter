import time
import naiv_bayes
import parser
import csv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
app = Flask(__name__)
cors = CORS(app)


def vk():
    domain = "degradination"
    at = 'ea51924dea51924dea51924decea2505dceea51ea51924db5c7ef7faa5701ef69eb57f0'
    while True:
        com_texts_users = parser.get_last_comment(domain, at)
        labeled_messages = naiv_bayes.classifier(com_texts_users.values())
        counter = 0
        for comment, toxic in labeled_messages:
            print('%r => %s' % (comment, toxic))
            if (counter == 50):
                break
            counter += 1
        time.sleep(60)


def write_csv(data):
    with open("group_comments_labeled.csv.csv", 'w', encoding='utf-8') as file:
        for line in data:
            a_pen = csv.writer(file)
            a_pen.writerow(line)


def read_csv():
    text = []
    with open("group_comments_labeled.csv") as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            text.append(line)
    return text


@app.route('/statistics', methods=['GET', 'POST'])
def get_statistics():
    domain = "degradination"
    at = 'ea51924dea51924dea51924decea2505dceea51ea51924db5c7ef7faa5701ef69eb57f0'
    com_texts_users = parser.get_last_comment(domain, at)
    labeled_messages = naiv_bayes.classifier(com_texts_users.values())

    t = 0
    nont = 0
    comment_toxic = []
    group_comments = []
    for comment, toxic in labeled_messages:
        comment_toxic.append({'Комментарий': comment, 'Токсичен': "Нет" if int(toxic) == 0 else "Да"})
        group_comments.append([comment, toxic])
        if int(toxic) == 0:
            nont += 1
        else:
            t += 1
    statistics_post = [t, nont]
    write_csv(group_comments)
    group_s = read_csv()
    t = 0
    nont = 0
    for i in group_s:
        if int(float(i[1])) == 0:
            nont += 1
        else:
            t += 1
    statistics_group = [t, nont]
    return jsonify([comment_toxic, statistics_group, statistics_post ])


if __name__ == '__main__':
    app.debug = True
    app.run()

