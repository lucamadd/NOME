from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_cors import cross_origin, CORS
import db_helper
import json

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
    return render_template('home.html',tracks = tracks, genres = json.dumps(db_helper.get_all_genres()), subgenres = db_helper.get_all_subgenres())

@app.route('/admin')
def admin():
    tracks = db_helper.get_first_tracks()
    return render_template('admin.html',tracks = tracks, genres = json.dumps(db_helper.get_all_genres()), subgenres = db_helper.get_all_subgenres())

@app.route('/song')
def song():
    track_id = request.args['song']
    track = db_helper.find_track_by_id(track_id)
    return render_template('song.html', track=track)

@app.route('/song_admin')
def song_admin():
    track_id = request.args['song']
    track = db_helper.find_track_by_id(track_id)
    return render_template('song_admin.html', track=track, genres = json.dumps(db_helper.get_all_genres()), subgenres = db_helper.get_all_subgenres())

@app.route('/new_song')
def new_song():
    return render_template('new_song.html', genres = json.dumps(db_helper.get_all_genres()), subgenres = db_helper.get_all_subgenres())

@app.route('/get_new_track_id', methods = ['GET', 'POST'])
def get_new_track_id():
    new_track_id = db_helper.get_new_track_id()
    return jsonify(new_track_id)


@app.route('/find_tracks', methods = ['GET', 'POST'])
def find_tracks():
    data = request.form
    tracks = db_helper.find_tracks(data)
    return jsonify(tracks)

@app.route('/find_tracks_admin', methods = ['GET', 'POST'])
def find_tracks_admin():
    data = request.form
    tracks = db_helper.find_tracks_admin(data)
    return jsonify(tracks)

@app.route('/save_song', methods = ['GET', 'POST'])
def save_song():
    data = request.form
    return jsonify(db_helper.insert_song(data))

@app.route('/delete_song', methods = ['GET', 'POST'])
def delete_song():
    data = request.form
    return jsonify(db_helper.delete_song(data))

@app.route('/update_song', methods = ['GET', 'POST'])
def update_song():
    data = request.form
    return jsonify(db_helper.update_song(data))

@app.errorhandler(500)
def internal_server_error(e):
    #set the 500 status explicitly
    return render_template('index.html')
    

if __name__ == '__main__':
    try:
        app.run(debug=True)
        
    except RuntimeError as msg:
        exit()