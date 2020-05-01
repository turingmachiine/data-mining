import lyricsgenius

genius = lyricsgenius.Genius("vRZ1JlhlTs-vb-rWoyF7mpl62dU1CD4gGHDzAKaNQ1drtGRBpl85gftCAWstFlBu")
artist = genius.search_artist("Baddie", max_songs=3, sort="popularity")
for song in artist.songs:
    print(song.title)