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

  docs = coll.find(query)
  if popularity != '' or popularity != '0':
    if popularity == '1': #most popular first
      docs = coll.find(query).sort('track_popularity', pymongo.DESCENDING)
    elif popularity == '2': #least popular first
      docs = coll.find(query).sort('track_popularity', pymongo.ASCENDING)
    

  for doc in docs:
    results.append(doc)

  print(results[0])



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




def ms_to_minutes(ms):
  seconds=int(ms/1000)%60
  minutes=int(ms/(1000*60))%60

  if seconds < 10:
    seconds = str(seconds)
    seconds = '0' + seconds 


  return f"{minutes}:{seconds}"


if __name__ == "__main__":
  get_all_genres()
