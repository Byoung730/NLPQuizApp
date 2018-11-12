
import random
import re
import string
import uuid

import spacy
from flask import Flask, render_template, request, session
from jinja2 import Template

vectors = spacy.load('en_vectors_web_lg')

origDoc = '''WHEN I WROTE the following pages, or rather the bulk of them, I lived alone, in the woods, a mile from any neighbor, in a house which I had built myself, on the shore of Walden Pond, in Concord, Massachusetts, and earned my living by the labor of my hands only. I lived there two years and two months. At present I am a sojourner in civilized life again.  I should not obtrude my affairs so much on the notice of my readers if very particular inquiries had not been made by my townsmen concerning my mode of life, which some would call impertinent, though they do not appear to me at all impertinent, but, considering the circumstances, very natural and pertinent. Some have asked what I got to eat; if I did not feel lonesome; if I was not afraid; and the like. Others have been curious to learn what portion of my income I devoted to charitable purposes; and some, who have large families, how many poor children I maintained. I will therefore ask those of my readers who feel no particular interest in me to pardon me if I undertake to answer some of these questions in this book. In most books, the I, or first person, is omitted; in this it will be retained; that, in respect to egotism, is the main difference. We commonly do not remember that it is, after all, always the first person that is speaking. I should not talk so much about myself if there were anybody else whom I knew as well. Unfortunately, I am confined to this theme by the narrowness of my experience. Moreover, I, on my side, require of every writer, first or last, a simple and sincere account of his own life, and not merely what he has heard of other men's lives; some such account as he would send to his kindred from a distant land; for if he has lived sincerely, it must have been in a distant land to me. Perhaps these pages are more particularly addressed to poor students. As for the rest of my readers, they will accept such portions as apply to them. I trust that none will stretch the seams in putting on the coat, for it may do good service to him whom it fits.'''

app = Flask(__name__, static_folder="../static",
            template_folder="../templates")
key = uuid.uuid4()
app.secret_key = str(key)
app.config['SESSION_TYPE'] = 'filesystem'


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html", data=origDoc)


correctAnswers = []


@app.route("/quiz", methods=['GET', 'POST'])
def quiz():
    try:
        def closeWords(word):
            words = [w for w in word.vocab if w.is_lower
                     == word.is_lower and w.prob >= -15]
            close = sorted(
                words, key=lambda w: word.similarity(w), reverse=True)
            # TODO: filter out words under 5 letters
            return close[:4]

        sentences1 = (request.form['input']).split('.')
        sentences = list(set(sentences1))
        noPunct = str.maketrans({}.fromkeys(string.punctuation))
        sentenceArray = []

        for sentence in sentences:
            noLittles = re.sub(r'\b\w{1,4}\b', '', sentence)
            filtered = (noLittles.translate(noPunct)).lower()
            noExtraSpaces = re.sub(' +', ' ', filtered)
            sentenceArray.append(noExtraSpaces)

        questionsArray = []
        answersArray = []
        i = 0

        def my_shuffle(array):
            random.shuffle(array)
            return array

        for sentence in sentenceArray:
            s_array = sentence.split(' ')
            if s_array:
                s_array2 = list(filter(lambda x: x != '', s_array))
                print(s_array2)
                if s_array2:
                    if i < len(sentenceArray) - 3:
                        if len(sentenceArray) > 3:
                            x = s_array2[len(s_array2) - 2]
                            if x.isalpha():
                                correctAnswers.append(x)
                                s_array2.pop(len(s_array2) - 2)
                                questionsArray.append(
                                    (sentences[i].lower()).replace(' ' + x.lower(), ' ' + '__________'))
                                answers = [w.lower_ for w in closeWords(
                                    vectors.vocab[x])]
                                if x in answers:
                                    answersArray.append(
                                        my_shuffle(answers))
                                else:
                                    del answers[1]
                                    answers.append(x)
                                    answersArray.append(
                                        my_shuffle(answers))
            i += 1

        session['answers'] = correctAnswers

        return render_template("quiz.html", data=request.form['input'], data2=questionsArray[0], data3=answersArray[0], data4=questionsArray[1], data5=answersArray[1], data6=questionsArray[2], data7=answersArray[2], data8=questionsArray[3], data9=answersArray[3], data10=questionsArray[4], data11=answersArray[4], data12=questionsArray[5], data13=answersArray[5], data14=questionsArray[6], data15=answersArray[6], data16=questionsArray[7], data17=answersArray[7], data18=questionsArray[8], data19=answersArray[8], data20=questionsArray[9], data21=answersArray[9], answers=correctAnswers)
    except Exception as e:
        if (str(e)) == 'list index out of range':
            return 'Either the document is too short to create a quiz, or the sentences in the document are too short to create questions -- try another please'
        return str(e)


@app.route("/grade", methods=['GET', 'POST'])
def grade():
    try:
        answers = session.get('answers', None)

        def grading():
            total = 0
            if answers[0] == request.form["1"]:
                total += 1
            if answers[1] == request.form["2"]:
                total += 1
            if answers[2] == request.form["3"]:
                total += 1
            if answers[3] == request.form["4"]:
                total += 1
            if answers[4] == request.form["5"]:
                total += 1
            if answers[5] == request.form["6"]:
                total += 1
            if answers[6] == request.form["7"]:
                total += 1
            if answers[7] == request.form["8"]:
                total += 1
            if answers[8] == request.form["9"]:
                total += 1
            if answers[9] == request.form["10"]:
                total += 1
            return total

        y = grading()

        def scoring(total):
            if total == 10:
                grade = 'A+'
            if total == 9:
                grade = 'A'
            if total == 8:
                grade = 'B'
            if total == 7:
                grade = 'C'
            if total == 6:
                grade = 'D'
            if total < 6:
                grade = 'F'
            return grade

        final = scoring(y)

        return render_template("grade.html", score1=request.form["1"], score2=request.form["2"], score3=request.form["3"], score4=request.form["4"], score5=request.form["5"], score6=request.form["6"], score7=request.form["7"], score8=request.form["8"], score9=request.form["9"], score10=request.form["10"], answers=answers, total=y, grade=final)
    except Exception as e:
        if (str(e)) == '400 Bad Request: The browser (or proxy) sent a request that this server could not understand.':
            return "Please answer all questions, even if you're not sure about the answer"
        return str(e)


if __name__ == "__main__":
    app.run(port='5000', debug=True)
