# importing libraries
import tekore as tk

def authorize():
     # create you're own client and client secret id from spotif developers api
     # kindly dont't use mine
     CLIENT_ID = "341a39d1ce444bfdb0e3ba80fb9e2775"
     CLIENT_SECRET = "c0ac6f3830994d10836e539008240801"
     # getting the app token
     app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
     # authorization completed
     return tk.Spotify(app_token)