import sys
import psycopg2
import lyricsgenius
import spacy


def lemmatize(text, artist_name, song_name):
    stop_list = [',', '.', '\'', '\"', "\n", "-PRON-", '-', '–', '...', '[', ']', '(', ')', '{', '}', ':', ';',
                 '?', '!', '#', 'i', 'i\'m', 'the', 'a', 'do', 'be', 'and', 'or', 'that', 'these', 'those', 'o', 'not'
                 'verse', '1', '2', '3', '4']
    text = text.lower()
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    sentencies = text.split('\n')
    for sentence in sentencies:
        doc = nlp(sentence)
        for word in doc:
            if stop_list.__contains__(word.lemma_) is False:
                query = list()
                query.append(word.lemma_)
                query.append(str(artist_name))
                query.append(str(song_name))
                cur.execute("INSERT INTO lyrics VALUES (%s, %s, %s)", query)
                print(word.lemma_)


def find_songs(artist_name, max_songs):
    artist = genius.search_artist(artist_name, max_songs=max_songs, sort="popularity")
    for song in artist.songs:
        lemmatize(song.lyrics, artist_name, song.title)


args = sys.argv
for arg in args:
    if arg == '-h':
        host = args[args.index(arg) + 1]
    elif arg == '-p':
        port = args[args.index(arg) + 1]
    elif arg == '-u':
        user = args[args.index(arg) + 1]
    elif arg == '-n':
        name = args[args.index(arg) + 1]
    elif arg == '-pass':
        password = args[args.index(arg) + 1]

con = psycopg2.connect(
    database=name,
    user=user,
    password=password,
    host=host,
    port=port,
)
con.autocommit = True
cur = con.cursor()
genius = lyricsgenius.Genius("vRZ1JlhlTs-vb-rWoyF7mpl62dU1CD4gGHDzAKaNQ1drtGRBpl85gftCAWstFlBu")
find_songs("The Weeknd", 3)
find_songs("Kendrick Lamar", 3)
find_songs("Tyler, The Creator", 3)
