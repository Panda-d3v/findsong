import time  # at the top of your file if not already
import sys  # for argv
import pydoc  # to show the lyrics
import warnings
from threading import Thread
import socket

import genius_api
import lyrics_store
import display
warnings.simplefilter(action='ignore', category=FutureWarning)


def is_connected_to_genius(timeout=3):
    try:
        socket.create_connection(("genius.com", 80), timeout=timeout)
        return True
    except OSError:
        return False


def main():
    token = genius_api.token
    if not token:
        print("❌ GENIUS_ACCESS_TOKEN not set in environment.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: findsong \"lyrics snippet or song name\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    online_available = is_connected_to_genius()
    mode = "online" if online_available else "offline"
    if mode == "offline":
        print("It looks like you are offline 🌵")

    ##########################################################################
    # 1. Try offline search first
    local_results = lyrics_store.search_local_songs(query)
    if len(local_results) == 0:
        if online_available:
            print("Going online")
        else:
            print("You are offline, couldn't find anything on device")
    else:
        print("\n🪵 Found in your local stash:")
        for i, song in enumerate(local_results):
            print(f"{i}️⃣ {song['artist']} – {song['title']}")
        selected = display.handle_selection(local_results, mode="offline")
        while True:
            if selected == "restart":
                new_input = input("😇 Trying again? Here you go: ")
                sys.argv = [sys.argv[0]] + new_input.split()
                return main()

            elif selected == "quit":
                return

            elif selected == "online" and online_available:
                break

            elif isinstance(selected, dict):
                pydoc.pager(selected["lyrics"])
                # does not break

            elif not online_available:
                print("🛑 No internet, and nothing else to find.")
                return

            selected = display.handle_selection(
                local_results, mode="offline", verbose=False)
    ###########################################################################
    # 2. Online search if not found locally, or if user chooses to continue
    results = False
    if online_available:
        results = genius_api.query_songs_genius(
            query, token, max_results=10)
    if not results:
        print("❌ No songs found.")
        return

    display.print_song_choices(results)

    # Background caching, always causing problems
    """
    def cache_top_song(song):
        def worker():
            if not lyrics_store.get_cached_lyrics(song['title'], song['artist']):
                with display.suppress_stdout():
                    lyrics = genius_api.fetch_lyrics_with_lyricsgenius(
                        song['title'], song['artist'])
                if lyrics:
                    lyrics_store.cache_lyrics(
                        song['title'], song['artist'], lyrics)
        Thread(target=worker, daemon=True).start()
    """

    def cache_top_song(song):
        print(f"📦 Caching: {song['artist']} – {
              song['title']}...", end="", flush=True)

        if not lyrics_store.get_cached_lyrics(song['title'], song['artist']):
            with display.suppress_stdout():
                lyrics = genius_api.fetch_lyrics_with_lyricsgenius(
                    song['title'], song['artist']
                )
            if lyrics:
                lyrics_store.cache_lyrics(
                    song['title'], song['artist'], lyrics)
                print(" ✅ Done.")
            else:
                print(" ❌ Failed to fetch lyrics.")
        else:
            print(" ✅ Already cached.")

    cache_top_song(results[0])

    selected = display.handle_selection(results, mode="online")
    while True:
        if selected == "restart":
            new_input = input("😇 Trying again? Here you go: ")
            sys.argv = [sys.argv[0]] + new_input.split()
            return main()
            # break
        elif selected == "remove":
            lyrics_store.remove_song(results[0])

        elif isinstance(selected, dict):
            lyrics = lyrics_store.get_cached_lyrics(
                selected["title"], selected["artist"]
            )
            if not lyrics:
                lyrics = genius_api.fetch_lyrics_with_lyricsgenius(
                    selected["title"], selected["artist"]
                )
                if lyrics:
                    lyrics_store.cache_lyrics(
                        selected["title"], selected["artist"], lyrics
                    )
                else:
                    print("Couldn't find lyrics")
                    break

            if lyrics:
                pydoc.pager(lyrics)  # then goes to selected = display ...

        elif selected == "quit":
            break

        selected = display.handle_selection(
            results, mode="online", verbose=False)


if __name__ == "__main__":
    main()
