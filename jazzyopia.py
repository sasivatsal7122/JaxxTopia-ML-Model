# importing libraries
import pandas as pd
import auth_sp as authorization
import numpy as np
from numpy.linalg import norm

class mood_based(object):
    # initialzing
    def __init__(self,file_path):
        # making instance dataframe
        self.VA_data_frame = pd.read_csv(file_path)
    # making a method global to call it from anywhere in the class
    global recommend
    def recommend(sorted_df):
        # making a list of id's from recommended songs
        id_list = []
        id_list = sorted_df["id"].tolist()
        id_list
        # making a list of tracks from recommended songs
        track_list = []
        track_list = sorted_df["track_name"].tolist()
        track_list
        # making a list of links from recommended songs
        links_list=[]
        for sid in id_list:
            # appending spotify song id in the url
            link = f'https://open.spotify.com/track/{sid}?si=77d73328f792498e'.format(sid)
            # appending the final song url into a list
            links_list.append(link)
        # making a list of artists from recommended songs    
        artist_name=[]
        artist_name = sorted_df["artist_name"].tolist()
        artist_name
        # printing similar songs
        print("\n====================================================================")
        print("Songs Recommendations based on you're current predicted mood are: ")
        print("====================================================================\n")
        # printing mood based recommended songs along with name,artist name and spotify link
        for i in range(5):
            print(f"                 {i+1}.{track_list[i]} by {artist_name[i]}\n")
            print(">play from here:",links_list[i])
            print("\n\n")
    
    # getting the authorization from spotify web api using tekore
    # after which it is used to request the valence-energy levels of user given song
     
    sp = authorization.authorize()
    
    # main driver method
    
    def recom_prep(self,track_id, sp=sp,):
        # creating a new coloumn of name mood_vec, which is the main recommendation system of this model
        # this coloumn contains x,y values as valence and energy which can be visualzied as x,y points in graph
        # this pair is the vector from which distance is calculated next
        self.VA_data_frame["mood_vec"] = self.VA_data_frame[["valence", "energy"]].values.tolist()
        # stroing the data frame into a copy dataframe, so that original remains uneffected
        ref_df=self.VA_data_frame
        # getting the track featues of the user given song by sending request to the spotify web api
        # using track_audio_features method in tkore module
        track_features = sp.track_audio_features(track_id)
        # making an array of valence and energy of user given song
        track_moodvec = np.array([track_features.valence, track_features.energy])
        # creating a new coloumn in copy dataframe with name distance
        # in this coloumn we will be storing the distances of x.y i.e the values of valence energy 
        # which i created earlier and stored in mood_vec coloumn
        ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec-np.array(x)))
        # sorting the distnaces in ascending order, since least distnace means more similar
        # the less the distanec with valence-energy of user given more similar the song
        ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)
        # removing the 1st result, coz 1st result is always the song given by the user
        # it's so dumb recommending the song given by the song
        ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]
        # taking only top 5 results, can be altered by changing the number to some x
        sorted_df = ref_df_sorted.iloc[:5]
        # calling the recommend method to print
        recommend(sorted_df)
    
# taking input from the user
user_song = input("Paste song URL: ")
# slicing the user to get the song id/token
track_id = user_song[31:53]
# creating an object of class mood-based and passing the dataset
fp = mood_based("valence_arousal_dataset.csv")
# calling recom_prep method in class mood_based from opbject fp
fp.recom_prep(track_id)