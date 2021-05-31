import csv, json

with open('spotify_songs_no_header.csv', 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)

    data = []
    i = 0

    for row in csv_reader:
        track_id = row[0]
        track_name = row[1]
        track_artist = row[2]
        track_popularity = row[3]
        track_album_id = row[4]
        track_album_name = row[5]
        track_album_release_date = row[6]
        playlist_name =row[7]
        playlist_id =row[8]
        playlist_genre =row[9]
        playlist_subgenre =row[10]
        danceability =row[11]
        energy =row[12]
        valence =row[13]
        tempo =row[14]
        duration_ms =row[15]

        data.append({
            'track_id': int(track_id),
            'track_name': track_name,
            'track_artist': track_artist,
            'track_popularity': int(track_popularity),
            'album': {
                'track_album_id': track_album_id,
                'track_album_name': track_album_name,
                'track_album_release_date': track_album_release_date
            },
            'playlist': {
                'playlist_name': playlist_name,
                'playlist_id': playlist_id,
                'playlist_genre': playlist_genre,
                'playlist_subgenre': playlist_subgenre
            },
            'danceability': float(danceability),
            'energy': float(energy),
            'valence': float(valence),
            'tempo': float(tempo),
            'duration_ms': int(duration_ms)
        })
        print(f"{i} of 32830")
        i = i+1

    with open('output.json', 'w') as outfile:
        json.dump(data, outfile)
