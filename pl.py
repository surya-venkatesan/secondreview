import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

auth_manager = SpotifyClientCredentials(client_id='d78eef8099514fdd9bdca35989ac0c1e', client_secret='f81ef7e025964716825b2c201bf41cc1')
sp = spotipy.Spotify(auth_manager=auth_manager)

playlist_code = input("Enter the Playlist Link: \n")
playlist_dict = sp.playlist(playlist_code)
print(json.dumps(playlist_dict, indent=4))
def get_track_features(track_id,sp):
    if track_id is None:
        return None
    else:
        features = sp.audio_features([track_id])
    return features

def get_features(tracks,sp):
    tracks_with_features=[]

    for track in tracks:
        # print(track[1])
        features = get_track_features(track[1],sp)
        # print (track[0])
        if not features:
            print("passing track %s" % track['name'])
            pass
        else:
            f = features[0]
            
            tracks_with_features.append(dict(
                                            name=track[0],
                                            artist=track[2],
                                            id=track[1],
                                            album=track[3],
                                            release_date=track[4],
                                            image_url=track[5],
                                            danceability=f['danceability'],
                                            energy=f['energy'],
                                            loudness=f['loudness'],
                                            speechiness=f['speechiness'],
                                            acousticness=f['acousticness'],
                                            tempo=f['tempo'],
                                            liveness=f['liveness'],
                                            valence=f['valence']
                                            ))

    # print(tracks_with_features[0])
    return tracks_with_features
no_of_songs = playlist_dict["tracks"]["total"]

album_list = []
song_list = []
release_date_list = []
artists_list = []
track_id_list = []
image_url_list = []
tracks = playlist_dict["tracks"]
items = tracks["items"]

i=0
while i<no_of_songs:
    
    song = items[i]["track"]["name"]
    track_id = items[i]["track"]["id"]
    album = items[i]["track"]["album"]["name"]
    release_date = items[i]["track"]["album"]["release_date"]
    artists = [k["name"] for k in items[i]["track"]["artists"]]
    image_url=items[i]['track']['album']['images'][1]['url']

    artists = ','.join(artists)
    track_id_list.append(track_id)
    album_list.append(album)
    song_list.append(song)
    release_date_list.append(release_date)
    artists_list.append(artists)
    image_url_list.append(image_url)
    i+=1
    if i==100:
        break
print(i)  
    
final_data = list(zip(song_list,track_id_list,artists_list,album_list,release_date_list,image_url_list))
# print(json.dumps(final_data, indent=4))
metadata = get_features(final_data,sp)
##print(json.dumps(metadata, indent=4))
##print(type(metadata))
final_value = []
for i in metadata:
    final_value.append(i.values())

import csv
Details = ["Name","Artists","Track_id","Album","Release Date", "Image_URL", "Danceability","Energy","Loudness","Speechiness","Acousticness","Tempo","Liveness","Valence"]
row = final_value
with open("chill4.csv",'w', newline='') as f, open("playlist1.json",'w', newline='') as g:
   write = csv.writer(f)
   write.writerow(Details)
   write.writerows(final_value)
   json.dump(metadata,g, indent=3)

f.close()



# if (i+1)%100 == 0:
#         tracks = sp.next(tracks)
#         items = tracks["items"]
#         offset = i+1
# https://open.spotify.com/playlist/37i9dQZF1DXbVhgADFy3im?si=75895f3362404d57
