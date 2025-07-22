from difflib import SequenceMatcher
import json
import os
import difflib

LYRICS_FILE = os.path.join(os.path.dirname(__file__), "my_songs.json")


def _load_lyrics_db():
    if not os.path.exists(LYRICS_FILE):
        return []
    with open(LYRICS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_lyrics_db(db):
    with open(LYRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)


def _normalize(s):
    return s.strip().lower()


def get_cached_lyrics(title, artist):
    db = _load_lyrics_db()
    for song in db:
        if _normalize(song["title"]) == _normalize(title) and _normalize(song["artist"]) == _normalize(artist):
            return song["lyrics"]
    return None


def cache_lyrics(title, artist, lyrics):
    db = _load_lyrics_db()

    # Avoid duplicates
    for song in db:
        if _normalize(song["title"]) == _normalize(title) and _normalize(song["artist"]) == _normalize(artist):
            return  # Already cached

    db.append({
        "title": title.strip(),
        "artist": artist.strip(),
        "lyrics": lyrics.strip(),
    })
    _save_lyrics_db(db)


def remove_song(song):
    db = _load_lyrics_db()
    target_title = _normalize(song['title'])
    target_artist = _normalize(song['artist'])

    match_index = None
    for i, s in enumerate(db):
        if _normalize(s['title']) == target_title and _normalize(s['artist']) == target_artist:
            match_index = i
            break

    if match_index is not None:
        removed = db.pop(match_index)
        _save_lyrics_db(db)
        print(f"🗑️ Removed: {removed['artist']} – {removed['title']}")
    else:
        print("❌ Song not found in database.")


def token_overlap_score(query_tokens, text_tokens):
    common = query_tokens & text_tokens
    if not common:
        return 0.0
    return len(common) / (len(common) + 1)


def adjacent_token_score(phrase, text, window=8):
    phrase_tokens = phrase.lower().split()
    text_tokens = text.lower().split()
    max_score = 0.0
    p_len = len(phrase_tokens)

    for i in range(len(text_tokens) - window + 1):
        window_tokens = text_tokens[i:i+window]
        match_count = sum(
            1 for j in range(min(p_len, window))
            if phrase_tokens[j] == window_tokens[j]
        )
        score = match_count / p_len
        max_score = max(max_score, score)

    return max_score


def score_query(query, title, artist, lyrics):
    query = query.lower().strip()
    lyrics_score = adjacent_token_score(query, lyrics)

    artist_in_query = artist.lower() in query
    artist_score = 1.0 if artist_in_query else 0.0

    # Small token overlap bonus (optional)
    query_tokens = set(query.split())
    all_tokens = set((title + " " + artist + " " + lyrics).lower().split())
    overlap_score = token_overlap_score(query_tokens, all_tokens)

    return (
        0.6 * lyrics_score +
        0.3 * overlap_score +
        0.1 * artist_score
    )


def search_local_songs(query, max_results=5, cutoff=0.5):
    db = _load_lyrics_db()
    matches = []

    query = query.lower().strip()

    for song in db:
        score = score_query(
            query,
            song.get("title", ""),
            song.get("artist", ""),
            song.get("lyrics", "")
        )

        if score >= cutoff:
            matches.append((score, song))

    matches.sort(key=lambda x: x[0], reverse=True)

    return [
        {
            "title": song["title"],
            "artist": song["artist"],
            "url": song.get("url", "🪵 from local stash"),
            "lyrics": song["lyrics"]
        }
        for _, song in matches[:max_results]
    ]
