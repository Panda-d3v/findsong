import sys


def parameter_cli(arg):

    # LIST
    if arg in ["-l", "--list"]:
        from lyrics_store import list_cached_songs
        list_cached_songs()
        return True

    # DELETE LAST

    elif arg in ["-rm"]:
        from lyrics_store import remove_cached_song_by_index, remove_last_cached_song

        if len(sys.argv) >= 3:
            try:
                index = int(sys.argv[2]) - 1  # make it 0-based
                remove_cached_song_by_index(index)
            except ValueError:
                print("❌ Invalid number. Usage: -rm [index]")
            except IndexError:
                print("❌ No song at that index.")
        else:
            remove_last_cached_song()
        return True
    # CLEAR ALL
    elif arg in ["-clear", "--clear"]:
        from lyrics_store import clear_all_songs
        clear_all_songs()
        return True

    elif arg in ['-h', '--help']:
        print("""
    🎧 findsong — the lyrical command-line companion 🤠

    Usage:
        findsong "some lyrics or song title"

    Options:
        -h, --help         Show this help message
        -l, --list      List all cached songs (offline library)
        -del, --delete     Remove the last cached song
        -clear, --clear    Delete all cached songs (with confirmation)
    """)
        return True
    else:
        return False
