import os
import requests
from lyricsgenius import Genius

token = os.getenv("GENIUS_ACCESS_TOKEN")

genius = Genius(token, remove_section_headers=True,
                skip_non_songs=True, verbose=False)


def query_songs_genius(query, access_token, max_results=5):
    """
    Search Genius API for a song using a query, return up to max_results options.

    Returns:
        list[dict]: Each dict has 'artist', 'title', 'url'.
    """
    base_url = "https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": query}

    response = requests.get(base_url, headers=headers, params=params)
    data = response.json()

    hits = data["response"]["hits"]
    results = []

    for hit in hits[:max_results]:
        result = hit["result"]
        artist_name = result["primary_artist"]["name"]
        song_title = result["title"]
        song_url = result["url"]
        results.append({
            "artist": artist_name,
            "title": song_title,
            "url": song_url
        })

    return results


def _clean_lyrics(raw_lyrics):
    marker = "Lyrics"
    idx = raw_lyrics.find(marker)
    if idx != -1:
        # Remove everything *up to and including* the marker line
        return raw_lyrics[idx + len(marker):].strip()
    return raw_lyrics.strip()


def fetch_lyrics_with_lyricsgenius(song_name, artist_name=None):
    """
    Uses Genius from lyricsgenius
    Makes it a bit slower but very handy for getting lyrics easily
    """
    genius = Genius(token, remove_section_headers=True, skip_non_songs=True)

    if artist_name:
        song = genius.search_song(song_name, artist_name)
    else:
        song = genius.search_song(song_name)

    if song:
        # return _clean_lyrics(song.lyrics)
        return _clean_lyrics(song.lyrics)
    else:
        print("❌ No song found.")
        return None
