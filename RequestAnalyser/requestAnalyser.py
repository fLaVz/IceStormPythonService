from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def hello():
    print("Hello World!")


@app.route("/", methods=['POST'])
def process():
    if request.form:
        an = Analyzer()
        print(request.data)
        an.analyzeAction(request.form["phrase"])
        return jsonify(
            action=an.action,
            song=an.song
        )


class Analyzer():

    action = "default"
    song = "default"

    def analyzeAction(self, phrase):
        if "joue" in phrase:
            self.action = "joue"
        elif "play" in phrase:
            self.action = "play"
        else:
            print("Phrase cannot be analyzed")
        self.analyzeMusic(phrase)

    def analyzeMusic(self, music):
        music = music.split(self.action + " ", 1)
        self.song = music[1]

    def printSong(self):
        print(self.action)
        print(self.song)

        #server launch:
        #export FLASK_APP=Analyzer.py
        #flask run
        #curl --data "phrase=play California love" http://127.0.0.1:5000