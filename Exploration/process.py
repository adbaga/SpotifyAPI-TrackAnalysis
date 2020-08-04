import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time 
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import os
import cred



class PlayListDownloader:                
    client_id = cred.client_id
    client_secret = cred.client_secret
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    def __init__(self,outputName, user, playlistid):  
        self.outputName = outputName
        self.user = user
        self.playlist_id = playlistid
        id = ''
        self.ids = self.getTrackIDs()
        self.tracks = self.getTrackFeatures()
        self.df = self.createTrackList()
    
    def getTrackIDs(self):
        ids = []
        playlist = PlayListDownloader.sp.user_playlist(self.user, self.playlist_id)
        for item in playlist['tracks']['items']:
            track = item['track']
            ids.append(track['id'])
            PlayListDownloader.ids = ids
        return ids
        

    def getTrackFeatures(self):
        tracks = []
        ids = self.ids
        for id in ids:
            time.sleep(.5)
            meta = PlayListDownloader.sp.track(id)
            features = PlayListDownloader.sp.audio_features(id)
            
            # metadata
            #more information: https://developer.spotify.com/documentation/web-api/reference/tracks/get-track/
            name = meta['name']
            album = meta['album']['name']
            artist = meta['album']['artists'][0]['name']
            release_date = meta['album']['release_date']
            length = meta['duration_ms']
            popularity = meta['popularity']

            # features of the music
            #more information: https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
            acousticness = features[0]['acousticness']
            danceability = features[0]['danceability']
            energy = features[0]['energy']
            instrumentalness = features[0]['instrumentalness']
            liveness = features[0]['liveness']
            loudness = features[0]['loudness']
            speechiness = features[0]['speechiness']
            tempo = features[0]['tempo']
            time_signature = features[0]['time_signature']
            valence = features[0]['valence']

            track = [name, album, artist, release_date, length, popularity,acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature,valence]
            tracks.append(track)
        
        return tracks
    
            

    def createTrackList(self):
        # create dataset
        df = pd.DataFrame(self.tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature','valence'])
        #Creating csv file from the dataFrame
        fileName = "spotify_{0}".format(self.outputName)
        df.to_csv("../data/"+fileName+".csv", sep = ',')
        return df
    
    def heatMap(self, plName='Playlist'):
        self.corr = self.df[['popularity','acousticness','danceability','energy','instrumentalness','liveness','tempo','valence']].corr()
        plName = plName
        mask = np.zeros_like(self.corr, dtype=np.bool)
        mask[np.triu_indices_from(mask)] = True
        sns.set(style='darkgrid')
        plt.figure(figsize=(12,8))
        ax = sns.heatmap(self.corr, annot=True, mask=mask)
        ax.collections[0].colorbar.set_label("{} heatmap".format(plName))