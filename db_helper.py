import pymongo

track_collection = None
db = None

def connect():

  myclient = pymongo.MongoClient("mongodb+srv://admin:admin@clusternome.9mulw.mongodb.net/NOME?retryWrites=true&w=majority")

  db = myclient["NOME"]

  collist = db.list_collection_names()
  if "track" in collist:
    print("The collection exists.")

  track_collection = db["track"]

def get_sixteen_random_tracks():
  myclient = pymongo.MongoClient("mongodb+srv://admin:admin@clusternome.9mulw.mongodb.net/NOME?retryWrites=true&w=majority")

  db = myclient["NOME"]

  pipeline = [
    {"$sample": {"size": 16}}
  ]

  results = db.track.aggregate(pipeline)


  tracks = []

  for result in results: 
    track = {}
    track['track_id'] = result['track_id']
    track['track_name'] = result['track_name']
    track['track_artist'] = result['track_artist']
    track['track_album_name'] = result['album']['track_album_name']
    track['duration'] = ms_to_minutes(int(result['duration_ms']))

    tracks.append(track)
    

  return tracks

def get_first_tracks():
  myclient = pymongo.MongoClient("mongodb+srv://admin:admin@clusternome.9mulw.mongodb.net/NOME?retryWrites=true&w=majority")

  db = myclient["NOME"]

  results = db.track.find().limit(12)


  tracks = []

  for result in results: 
    track = {}
    track['track_id'] = result['track_id']
    track['track_name'] = result['track_name']
    track['track_artist'] = result['track_artist']
    track['track_album_name'] = result['album']['track_album_name']
    track['duration'] = ms_to_minutes(int(result['duration_ms']))
    track['track_popularity'] = result['track_popularity']

    tracks.append(track)
    

  return tracks

def find_track_by_id(track_id):
  myclient = pymongo.MongoClient("mongodb+srv://admin:admin@clusternome.9mulw.mongodb.net/NOME?retryWrites=true&w=majority")

  db = myclient["NOME"]

  coll = db['track']

  query = { "track_id": int(track_id) }

  doc = coll.find(query)

  track = doc[0]

  track['duration_ms'] = ms_to_minutes(track['duration_ms'])

  return track

def find_tracks(data):
  myclient = pymongo.MongoClient("mongodb+srv://admin:admin@clusternome.9mulw.mongodb.net/NOME?retryWrites=true&w=majority")

  db = myclient["NOME"]

  coll = db['track']

  results = []

  page = data['page']  # inizialmente 1

  if data == None:
    return 'error'
  track_name = data['title']
  track_artist = data['artist']
  track_album = data['album']
  year = data['year']

  if data['month'] != '':
    if int(data['month']) < 10:
      month = '0' + data['month']
    else:
      month = data['month']
  else:
    month = ''
  duration = data['duration']
  genre = data['genre']
  subgenre = data['subgenre']
  popularity = data['popularity']

  query = {}
  docs = None

  if track_name != '':
    query['track_name'] = {
      "$regex": f'\\b{track_name}\\b',
      "$options" :'i'}

  if track_artist != '':
    query['track_artist'] = {
      "$regex": f'\\b{track_artist}\\b',
      "$options" :'i'}

  if track_album != '':
    query['album.track_album_name'] = {
      "$regex": f'\\b{track_album}\\b',
      "$options" :'i'}
  
  if year != '':
    if month == '' or month == '00':
      query['album.track_album_release_date'] = {
      "$regex": f'^{year}'}
    else:
      query['album.track_album_release_date'] = {
      "$regex": f'^{year}-{month}'}
      
  if duration != '' or duration != '0':
    if duration == '1': #meno di 2 minuti
      query['duration_ms'] = {
        "$lte": 120000 
      }
    elif duration == '2': #tra 2 e 3 minuti
      query['duration_ms'] = {
        "$gte": 120000,
        "$lte": 180000 
      }
    elif duration == '3': #tra 3 e 4 minuti
      query['duration_ms'] = {
        "$gte": 180000,
        "$lte": 240000 
      }
    elif duration == '4': #più di 4 minuti
      query['duration_ms'] = {
        "$gte": 240000 
      }

  if genre != '' and genre != '0':
    query['playlist.playlist_genre'] = genre

  if subgenre != '' and subgenre != '0':
    query['playlist.playlist_subgenre'] = subgenre

  docs = coll.find(query).skip((int(page))*12).limit(12)
  if popularity != '' or popularity != '0':
    if popularity == '1': #most popular first
      docs = coll.find(query).skip((int(page))*12).limit(12).sort('track_popularity', pymongo.DESCENDING)
    elif popularity == '2': #least popular first
      docs = coll.find(query).skip((int(page))*12).limit(12).sort('track_popularity', pymongo.ASCENDING)
    

  for doc in docs:
    doc.pop('_id')
    doc['duration_ms'] = ms_to_minutes(doc['duration_ms'])
    results.append(doc)



  return results

def find_tracks_admin(data):
  myclient = pymongo.MongoClient("mongodb+srv://admin:admin@clusternome.9mulw.mongodb.net/NOME?retryWrites=true&w=majority")

  db = myclient["NOME"]

  coll = db['track']

  results = []

  page = data['page']  # inizialmente 1

  if data == None:
    return 'error'
  track_name = data['title']
  track_artist = data['artist']
  track_id = data['track_id']


  query = {}
  docs = None

  if track_name != '':
    query['track_name'] = {
      "$regex": f'\\b{track_name}\\b',
      "$options" :'i'}

  if track_artist != '':
    query['track_artist'] = {
      "$regex": f'\\b{track_artist}\\b',
      "$options" :'i'}

  if track_id != '':
    query['track_id'] = int(track_id)
  
  

  docs = coll.find(query).skip((int(page))*12).limit(12)
    

  for doc in docs:
    doc.pop('_id')
    doc['duration_ms'] = ms_to_minutes(doc['duration_ms'])
    results.append(doc)


  return results

def get_all_genres():
  genres = []

  myclient = pymongo.MongoClient("mongodb+srv://admin:admin@clusternome.9mulw.mongodb.net/NOME?retryWrites=true&w=majority")

  db = myclient["NOME"]

  coll = db['track']

  for genre in coll.find().distinct('playlist.playlist_genre'):
    genres.append(genre)


  return genres

def get_all_subgenres():
  subgenres = []

  myclient = pymongo.MongoClient("mongodb+srv://admin:admin@clusternome.9mulw.mongodb.net/NOME?retryWrites=true&w=majority")

  db = myclient["NOME"]

  coll = db['track']

  for subgenre in coll.find().distinct('playlist.playlist_subgenre'):
    subgenres.append(subgenre)


  return subgenres


def get_new_track_id():
  myclient = pymongo.MongoClient("mongodb+srv://admin:admin@clusternome.9mulw.mongodb.net/NOME?retryWrites=true&w=majority")

  db = myclient["NOME"]

  docs = db.track.find().sort('track_id', pymongo.DESCENDING).limit(1)

  result = None

  for doc in docs:
    result = doc

  return result['track_id'] + 1

def insert_song(data):
  myclient = pymongo.MongoClient("mongodb+srv://admin:admin@clusternome.9mulw.mongodb.net/NOME?retryWrites=true&w=majority")

  db = myclient["NOME"]

  if data == None:
    return False

  track_id = int(data['track_id'])
  track_name = data['track_name']
  track_artist = data['track_artist']
  track_popularity = int(data['track_popularity'])
  track_album_id = data['track_album_id']
  track_album_name = data['track_album_name']
  track_album_release_date = data['track_album_release_date']
  track_playlist_name = data['track_playlist_name']
  track_playlist_id = data['track_playlist_id']
  track_playlist_genre = data['track_playlist_genre']
  track_playlist_subgenre = data['track_playlist_subgenre']
  track_danceability = float(data['track_danceability'])
  track_energy = float(data['track_energy'])
  track_valence = float(data['track_valence'])
  track_tempo = float(data['track_tempo'])
  track_duration_min = int(data['track_duration_min'])
  track_duration_sec = int(data['track_duration_sec'])

  #trasformo in ms
  track_duration_sec = track_duration_sec + track_duration_min*60
  track_duration_ms = track_duration_sec * 1000

  #inserisco nel db
  doc = {'track_id': track_id, 'track_name': track_name, 'track_artist': track_artist,
         'track_popularity': track_popularity, 'album': {'track_album_id': track_album_id,
          'track_album_name': track_album_name, 'track_album_release_date': track_album_release_date},
          'playlist': {'playlist_name': track_playlist_name, 'playlist_id': track_playlist_id,
          'playlist_genre': track_playlist_genre, 'playlist_subgenre': track_playlist_subgenre},
          'danceability': track_danceability, 'energy': track_energy, 'valence':track_valence, 'tempo': track_tempo,
          'duration_ms': track_duration_ms}

  result = db.track.insert_one(doc)
  if result.inserted_id:
    return True
  return False


def delete_song(data):
  myclient = pymongo.MongoClient("mongodb+srv://admin:admin@clusternome.9mulw.mongodb.net/NOME?retryWrites=true&w=majority")

  db = myclient["NOME"]
  track_id = int(data['track_id'])

  result = db.track.delete_one({'track_id': track_id})
  if result.deleted_count == 1:
    return True
  return False

def update_song(data):
  myclient = pymongo.MongoClient("mongodb+srv://admin:admin@clusternome.9mulw.mongodb.net/NOME?retryWrites=true&w=majority")

  db = myclient["NOME"]

  if data == None:
    return False

  track_id = int(data['track_id'])
  track_name = data['track_name']
  track_artist = data['track_artist']
  track_popularity = int(data['track_popularity'])
  track_album_id = data['track_album_id']
  track_album_name = data['track_album_name']
  track_album_release_date = data['track_album_release_date']
  track_playlist_name = data['track_playlist_name']
  track_playlist_id = data['track_playlist_id']
  track_playlist_genre = data['track_playlist_genre']
  track_playlist_subgenre = data['track_playlist_subgenre']
  track_danceability = float(data['track_danceability'])
  track_energy = float(data['track_energy'])
  track_valence = float(data['track_valence'])
  track_tempo = float(data['track_tempo'])
  track_duration_min = int(data['track_duration_min'])
  track_duration_sec = int(data['track_duration_sec'])

  #trasformo in ms
  track_duration_sec = track_duration_sec + track_duration_min*60
  track_duration_ms = track_duration_sec * 1000

  filter = { 'track_id': track_id }
    
  # Values to be updated.
  newvalues = { "$set": { 'track_name': track_name, 'track_artist': track_artist,
         'track_popularity': track_popularity, 'album': {'track_album_id': track_album_id,
          'track_album_name': track_album_name, 'track_album_release_date': track_album_release_date},
          'playlist': {'playlist_name': track_playlist_name, 'playlist_id': track_playlist_id,
          'playlist_genre': track_playlist_genre, 'playlist_subgenre': track_playlist_subgenre},
          'danceability': track_danceability, 'energy': track_energy, 'valence':track_valence, 'tempo': track_tempo,
          'duration_ms': track_duration_ms } }
    
  # Using update_one() method for single 
  # updation.
  result = db.track.update_one(filter, newvalues) 

  return result.matched_count > 0 
  









def ms_to_minutes(ms):
  seconds=int(ms/1000)%60
  minutes=int(ms/(1000*60))%60

  if seconds < 10:
    seconds = str(seconds)
    seconds = '0' + seconds 


  return f"{minutes}:{seconds}"



