
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from gamedata import load_data
from gamedata import update_data

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
@app.route('/')
def index():
    return '<style>li.genre{  background-image: url("static/src/assets/genre.svg")}li.system{  background-image: url("static/src/assets/system.svg")}li.publisher{  background-image: url("static/src/assets/publisher.svg")}li.game{  background-image: url("static/src/assets/game.svg")}@font-face {  font-family: "gameing-simulator";  src:  url("static/src/assets/fonts/gameing-simulator.eot?qhfh8m");  src:  url("static/src/assets/fonts/gameing-simulator.eot?qhfh8m#iefix") format("embedded-opentype"),    url("static/src/assets/fonts/gameing-simulator.ttf?qhfh8m") format("truetype"),    url("static/src/assets/fonts/gameing-simulator.woff?qhfh8m") format("woff"),    url("static/src/assets/fonts/gameing-simulator.svg?qhfh8m#gameing-simulator") format("svg");  font-weight: normal;  font-style: normal;}[class^="gaming-sim"], [class*=" gaming-sim"] {  /* use !important to prevent issues with browser extensions that change fonts */  font-family: "gameing-simulator" !important;  speak: none;  font-style: normal;  font-weight: normal;  font-variant: normal;  text-transform: none;  line-height: 1;  /* Better Font Rendering =========== */  -webkit-font-smoothing: antialiased;  -moz-osx-font-smoothing: grayscale;}.gaming-simabout:before {  content: "\e900";}.gaming-simgame:before {  content: "\e901";}.gaming-simgenre:before {  content: "\e902";}.gaming-simhelp:before {  content: "\e903";}.gaming-simoptions:before {  content: "\e904";}.gaming-simpublisher:before {  content: "\e905";}.gaming-simsystem:before {  content: "\e906";}</style><div id="app"></div><script src="static/dist/build.js"></script>'
@app.route('/contact')
def contact():
    return '<table><tr><td>hello</td><td>games</td></tr></table>'
@app.route('/data', methods=['GET'])
def data():
    print request
    response = jsonify(load_data())#({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/update', methods=['GET'])
def update():
    response = jsonify(update_data(request))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
if __name__ == "__main__":
    app.run()