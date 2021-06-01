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


def ms_to_minutes(ms):
  seconds=int(ms/1000)%60
  minutes=int(ms/(1000*60))%60

  if seconds < 10:
    seconds = str(seconds)
    seconds = '0' + seconds


  return f"{minutes}:{seconds}"

