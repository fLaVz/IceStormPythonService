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


class Analyzer:

    actionlist = ['play', 'lire', 'jouer', 'joue', 'ecouter', 'écouter', 'run', 'launch', 'listen']
    action = "default"
    song = "default"

    def analyzeAction(self, phrase):
        for i in range(0, len(self.actionlist)):
            if self.actionlist[i] in phrase:
                self.action = self.actionlist[i]
                self.analyzeMusic(phrase)
                self.action = 'play'
            else:
                print("Phrase cannot be analyzed")

    def analyzeMusic(self, music):
        music = music.split(self.action + " ", 1)
        self.song = music[1]

    def printSong(self):
        print(self.action)
        print(self.song)

        #server launch:
        #export FLASK_APP=requestAnalyzer.py or SET (windows)
        #flask run
        #curl --data "phrase=play California love" http://127.0.0.1:5000