import csv
import cPickle as pickle

artists = pickle.load(open("C:\Users\jbellmas\Documents\Kauffman drive\Code\\billboard_hot_100_May_24_2016.p","rb"))

with open("billboard_hot_100_MayClass_Scrape.csv","wb") as f:
          w = csv.writer(f)

          header = ['Rank', 'Artist Name', 'Song Title']
          w.writerow(header)

          for rank in artists:
              artistName = artists[rank]['artist_name']
              songTitle = artists[rank]['song_title']
              currentLine = [rank, artistName, songTitle]
              w.writerow([unicode(s).encode("utf-8") for s in currentLine])
                                        
