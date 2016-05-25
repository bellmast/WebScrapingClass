import urllib2
from bs4 import BeautifulSoup
import cPickle as pickle

try:
    artists = pickle.load(open("C:\Users\jbellmas\Documents\Kauffman drive\Code\\billboard_hot_100_May_24_2016.p","rb"))
except IOError:
    artists = {}

bbUrl = 'http://www.billboard.com/charts/hot-100'
req = urllib2.Request(bbUrl)
resp = urllib2.urlopen(req)

soup = BeautifulSoup(resp)

for i in range(1,101):
    print i

    layer1 = soup.find(class_="chart-row chart-row--%d js-chart-row"%(i))

    try:
        rankLayer2 = layer1.find(class_="chart-row__current-week")
    except AttributeError:
        layer1 = soup.find(class_="chart-row row-new chart-row--%d js-chart-row"%(i))
        rankLayer2 = layer1.find(class_="chart-row__current-week")
        
    currentRank = rankLayer2.contents[0].strip()

    if currentRank not in artists:
        
        artistLayer2 = layer1.find(class_="chart-row__artist")
        currentArtist = artistLayer2.contents[0].strip()

        songLayer2 = layer1.find(class_="chart-row__song")
        currentSong = songLayer2.contents[0].strip()

        artists[str(currentRank)] = {}
        artists[currentRank]['song_title'] = str(currentSong)
        artists[currentRank]['artist_name'] = str(currentArtist)

        pickle.dump(artists, open("C:\Users\jbellmas\Documents\Kauffman drive\Code\\billboard_hot_100_May_24_2016.p", "wb"))
