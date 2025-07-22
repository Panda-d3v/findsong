import pydoc
import contextlib
import io


@contextlib.contextmanager
def suppress_stdout():
    with contextlib.redirect_stdout(io.StringIO()):
        yield


def handle_selection(results, mode, verbose=True):
    """ returns a dictionary if something is selected.
        else returns a string:
        quit, restart, online
        can show more results if online
    """
    if verbose:
        print("\nWhat would you like to do next?\n")
        print("👉 [ y ]     see lyrics for the top pick")
        print("👉 [ 0–n ]   pick another song")
        if mode == "offline":
            print("👉 [ online ]  go online to find the song")
        elif mode == "online":
            print("👉 [ more ]  see more songs")
            print("👉 [ remove ]  removes the song that was automatically downloaded")
        print("👉 [ r ]     restart and type again")
        print("👉 [ q ]     quit\n")

    while True:
        choice = input("Say the call boss: ").strip().lower()
        idx = 0 if choice == "y" else int(choice) if choice.isdigit() else None

        if choice == "q":
            print("👋 Exiting.")
            return "quit"

        elif choice == "r":
            return "restart"

        elif choice == "remove":
            return "remove"

        elif choice == "online":
            return "online"

        elif choice == "more" and mode == "online":
            for idx, song in enumerate(results[6:], 6):
                print(f"{idx}️⃣ . {song['artist']} – {song['title']}")
            continue

        elif idx is not None and 0 <= idx < len(results):
            return results[idx]

        print("❌ Invalid input. Try 'y', a number, 'r', or 'q'.")


def print_song_choices(results):
    """
    Pretty-print a list of Genius search results in a warm, country style.
    """
    if not results:
        print("❌ No songs found.")
        return
    print("────────────────────────────")

    print("\nWell, partner, here’s what I found for ya:\n")

    print("✅ Most likely:")
    print(f"    🎤 Artist: {results[0]['artist']}")
    print(f"    🎵 Song  : {results[0]['title']}\n")

    # Collect alternatives (up to 5) while skipping the first result
    alternatives = [song for idx, song in enumerate(
        results) if idx != 0 and idx <= 5]

    if alternatives:
        print("🪉But it could also be:\n")
        for idx, song in enumerate(alternatives, 1):
            print(f"    {idx}️⃣ . 🎵 {song['artist']} – {song['title']}")
            # the weird character there allows to do 1, 2, 3 in unicode ?
        print()
