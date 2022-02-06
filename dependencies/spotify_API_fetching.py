# Import modules
import sys
sys.path.append("../jazztopia")
import auth_sp as authorization
import pandas as pd
from tqdm import tqdm
import time

# Authorize and call access object "sp"
# SP contains tk.Spotify(app_token) with my app token
sp = authorization.authorize()
# Getting all genres in the spotify database
genres = sp.recommendation_genre_seeds()
# Set number of recommendations per genre
n_recs = 100
# Initiating a dictionary with all the information needed for mood-based recommendation
# this dictionary is later used for creating a dataset with all the songs from spotify database
data_dict = {"id":[], "genre":[], "track_name":[], "artist_name":[],
             "valence":[], "energy":[]}
# Get recs for every genre
'''
tqdm is a Python library that allows you to output a smart progress bar 
by wrapping around any iterable. A tqdm progress bar not only shows you how much time
has elapsed, but also shows the estimated time remaining for the iterable.
'''
for genre in tqdm(genres):
    
    # Getting 100 recommendations
    records = sp.recommendations(genres = [genre], limit = n_recs)
    # json-like string to dict
    records = eval(records.json().replace("null", "-999").replace("false", "False").replace("true", "True"))["tracks"]
    
    # getting data from each song and storing it in it's respective key in dictionary
    for track in records:
        # ID and Genre
        data_dict["id"].append(track["id"])
        data_dict["genre"].append(genre)
        # Metadata
        track_meta = sp.track(track["id"])
        data_dict["track_name"].append(track_meta.name)
        data_dict["artist_name"].append(track_meta.album.artists[0].name)
        # Valence and energy
        track_features = sp.track_audio_features(track["id"])
        data_dict["valence"].append(track_features.valence)
        data_dict["energy"].append(track_features.energy)
        
        # Waiting 0.2 seconds per track so that the api doesnt overheat
        # No spamming the API BIXCHH!!
        time.sleep(0.2)
        
# Storing the data in dataframe
df = pd.DataFrame(data_dict)

# Dropping duplicates if any using drop-duplicates method in pandas
df.drop_duplicates(subset = "id", keep = "first", inplace = True)
# saving the dataframe to current working directory using to_csv method in pandas
df.to_csv("valence_arousal_dataset.csv", index = False)