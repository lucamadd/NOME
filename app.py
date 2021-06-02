from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_cors import cross_origin, CORS
import db_helper

app = Flask(__name__,
            static_url_path='', 
            static_folder='static')
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
@app.route('/index')
def index():
    tracks = db_helper.get_sixteen_random_tracks()
    return render_template('index.html', tracks = tracks)

@app.route('/home')
def home():
    tracks = db_helper.get_first_tracks()
    return render_template('home.html',tracks = tracks)

@app.route('/song')
def song():
    track_id = request.args['song']
    track = db_helper.find_track_by_id(track_id)
    return render_template('song.html', track=track)


@app.route('/find_tracks', methods = ['GET', 'POST'])
def find_tracks():
    data = request.form
    print(data)
    return 'ok'

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
        
    except RuntimeError as msg:
        exit()