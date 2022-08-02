import requests
import youtube_dl
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from requests_html import HTMLSession

def run( choice ):
    my_client_id='-'
    my_client_secret='-'


    

    print('starting csv creation ')

    OAuthObject = spotipy.SpotifyOAuth(
            client_id=my_client_id,
            client_secret=my_client_secret,
            redirect_uri='https://www.google.com/',
            scope="user-library-read")

    token_dict= OAuthObject.get_cached_token() #get access token instead 

    #print(token_dict[token_type])
    sp = spotipy.Spotify(auth=token_dict['access_token'])
    #https://www.google.com/?code=AQDVh5-PkYoXstAKXZixej0vTwB489BQRESdrKEY6rT4wWkJyYVkMJR5QEk1V2U7MMiQgViB7YbLOBy-vcdjsxDBifAsq47Bnh5IVDJUO8AeA11sqnktt9Zu9bnbB_sJVI6rMOw3y6wSgc8jzYCiAMmtgSoCU76IntBRqKbTyJ4h0Vm-ajyNOejdmmFClw

    results = []
    iter = 0
    print('track names being downloaded')
    if choice==1 :
        while True:
                offset = iter * 50
                iter += 1
                curGroup = sp.current_user_saved_tracks(limit=50, offset=offset)['items']
                for idx, item in enumerate(curGroup):
                    track = item['track']
                    print(track['name']+' '+track['artists'][0]['name'])
                    val = track['name'] + " - " + track['artists'][0]['name']
                    results += [val]
                if (len(curGroup) < 50):
                    break
        df = pd.DataFrame(results, columns=["song names"]) 
        df.to_csv('songs2.csv', index=False)
    else:
        artistid= input('give the artist id : ')
        artistname=sp.artist(artistid)['name']
        while True:
            offset = iter * 50
            iter += 1
            i=0
            
            
            topten = sp.artist_top_tracks(artistid)['tracks']
            for idx, item in enumerate(topten):
                track = item['name']
                print(track)
                val = track
                results += [val]
                i +=1
            if (len(topten) < 50):
                break
        df = pd.DataFrame(results, columns=["song names"]) 
        df.to_csv('Top Ten Songs by '+artistname+'.csv', index=False)












    print('starting download ')
    if choice==1:
        data = pd.read_csv('songs.csv')
        data = data['song names'].tolist()

        print("Found ", len(data), " songs!")

    else :
        data = pd.read_csv('Top Ten Songs by '+artistname+'.csv')
        data = data['song names'].tolist()

        print("Found ", len(data), " songs!")

    ids=[]
    
        
    
    def ScrapeVidId(query):
        print ("Getting video id for: ", query)
        BASIC="http://www.youtube.com/results?search_query="
        URL = (BASIC + query)
        URL.replace(" ", "+")
        page = requests.get(URL)
        session = HTMLSession()
        response = session.get(URL)
        response.html.render(sleep=1)
        soup = BeautifulSoup(response.html.html, "html.parser")

        results = soup.find('a', id="video-title")
        
        return results['href'].split('/watch?v=')[1]  

    def DownloadVideosFromIds(songs):
        SAVE_PATH = str(os.path.join(Path.home(), "Downloads/songs"))
        if os.path.isdir(SAVE_PATH):
            print('directoty exists')
        else:
            os.mkdir(SAVE_PATH)


	    

        BASE = 'https://www.youtube.com/watch?v='
        for index, item in enumerate(songs):
            URL=BASE+item
            print(URL)
        
            video_info = youtube_dl.YoutubeDL().extract_info(
            url = URL,download=False)
            filename = f"{video_info['title']}.mp3"
            options={
              'format':'bestaudio/best',
              'keepvideo':False,
              'outtmpl': SAVE_PATH + '/%(title)s.%(ext)s',
            }
        
            with youtube_dl.YoutubeDL(options) as ydl:
             ydl.download([video_info['webpage_url']])

    #print("Download complete... {}".format(filename))      

    for index, item in enumerate(data[0:1]):
        vid_id = ScrapeVidId(item)
        print(vid_id)
        ids += [vid_id]
    DownloadVideosFromIds(ids)
    
    #
    
    
    
    
    
if __name__=='__main__':
    while True:
        choice= input(' -1 to download your saved tracks  -2 to download top ten tracks from your chosen artist  :')
        
        if int(choice) ==1 or int(choice)==2 :
            
            run(choice)
        else :
            print('choice invalid')