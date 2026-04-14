"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {
        "genre":               "lofi",
        "mood":                "focused",
        "target_energy":       0.40,
        "target_acousticness": 0.75,
        "target_tempo_bpm":    82,
        "target_valence":      0.58,
        "target_danceability": 0.60,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    width = 60
    print()
    print("=" * width)
    print(" MUSIC RECOMMENDER — TOP PICKS")
    print(f" Profile: {user_prefs['genre'].upper()} / {user_prefs['mood'].upper()}"
          f"  |  energy target: {user_prefs['target_energy']}")
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f"  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Score: {score:.2f} / 7.00")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}"
              f"  |  Energy: {song['energy']}  |  BPM: {int(song['tempo_bpm'])}")
        print("       Why recommended:")
        for reason in explanation.split(" | "):
            print(f"         • {reason}")
        print("  " + "-" * (width - 2))

    print()


if __name__ == "__main__":
    main()
