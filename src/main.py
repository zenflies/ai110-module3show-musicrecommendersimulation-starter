"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

# ---------------------------------------------------------------------------
# User preference profiles
# ---------------------------------------------------------------------------

# Profile 1 — High-Energy Pop
# A gym-goer who wants fast, upbeat, danceable pop to power through a workout.
HIGH_ENERGY_POP = {
    "genre":               "pop",
    "mood":                "energetic",
    "target_energy":       0.92,
    "target_acousticness": 0.10,
    "target_tempo_bpm":    145,
    "target_valence":      0.85,
    "target_danceability": 0.90,
}

# Profile 2 — Chill Lofi
# A student studying late at night who wants mellow, acoustic-leaning beats.
CHILL_LOFI = {
    "genre":               "lofi",
    "mood":                "focused",
    "target_energy":       0.40,
    "target_acousticness": 0.75,
    "target_tempo_bpm":    82,
    "target_valence":      0.58,
    "target_danceability": 0.60,
}

# Profile 3 — Deep Intense Rock
# A headbanger who wants slow-burning, heavy, low-valence rock.
DEEP_INTENSE_ROCK = {
    "genre":               "rock",
    "mood":                "angry",
    "target_energy":       0.88,
    "target_acousticness": 0.08,
    "target_tempo_bpm":    120,
    "target_valence":      0.20,
    "target_danceability": 0.35,
}

# ---------------------------------------------------------------------------
# Adversarial / edge-case profiles  (System Evaluation)
# ---------------------------------------------------------------------------

# Edge case A — Contradictory Energy vs. Mood
# High physical energy but a sad emotional mood. Tests whether the scorer
# can surface a song that satisfies the numeric energy target even when the
# mood label is the opposite of what "energetic" typically implies.
CONFLICTED_SAD_HYPE = {
    "genre":               "pop",
    "mood":                "sad",           # mood label conflicts with energy
    "target_energy":       0.90,            # very high energy
    "target_acousticness": 0.15,
    "target_tempo_bpm":    140,
    "target_valence":      0.10,            # extremely low valence (dark feel)
    "target_danceability": 0.80,
}

# Edge case B — All Midpoint / Neutral
# Every numerical target is exactly 0.5 and BPM is centred. Tests whether
# the scorer handles a "no preference" user gracefully (no genre/mood bonus).
NEUTRAL_NO_PREFERENCE = {
    "genre":               "",              # no genre preference
    "mood":                "",              # no mood preference
    "target_energy":       0.50,
    "target_acousticness": 0.50,
    "target_tempo_bpm":    106,             # midpoint of [55, 158]
    "target_valence":      0.50,
    "target_danceability": 0.50,
}

# Edge case C — Extreme Acoustic Seeker in a Non-Acoustic Genre
# Requests a rock song (genre bonus) but wants near-silence acousticness.
# Checks whether genre weight can override a poor acousticness match.
ACOUSTIC_ROCKER = {
    "genre":               "rock",
    "mood":                "happy",
    "target_energy":       0.30,            # low energy for rock
    "target_acousticness": 0.95,            # nearly fully acoustic
    "target_tempo_bpm":    70,
    "target_valence":      0.75,
    "target_danceability": 0.40,
}

# Edge case D — Out-of-Range BPM Boundary
# Target BPM is at the very edge of the normalisation range (158 BPM).
# Validates that the tempo normalisation doesn't produce negative or >1 scores.
BOUNDARY_BPM = {
    "genre":               "pop",
    "mood":                "energetic",
    "target_energy":       0.95,
    "target_acousticness": 0.05,
    "target_tempo_bpm":    158,             # max of normalisation range
    "target_valence":      0.90,
    "target_danceability": 0.95,
}

# ---------------------------------------------------------------------------
# All profiles to run, with display labels
# ---------------------------------------------------------------------------
ALL_PROFILES = [
    ("High-Energy Pop",             HIGH_ENERGY_POP),
    ("Chill Lofi",                  CHILL_LOFI),
    ("Deep Intense Rock",           DEEP_INTENSE_ROCK),
    # --- adversarial ---
    ("[EDGE] Contradictory Sad Hype",       CONFLICTED_SAD_HYPE),
    ("[EDGE] Neutral / No Preference",      NEUTRAL_NO_PREFERENCE),
    ("[EDGE] Acoustic Rocker",              ACOUSTIC_ROCKER),
    ("[EDGE] Boundary BPM (158)",           BOUNDARY_BPM),
]


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k)

    width = 60
    genre_display = user_prefs["genre"].upper() if user_prefs["genre"] else "ANY"
    mood_display  = user_prefs["mood"].upper()  if user_prefs["mood"]  else "ANY"

    print()
    print("=" * width)
    print(f" PROFILE: {label}")
    print(f" Genre: {genre_display}  |  Mood: {mood_display}"
          f"  |  Energy target: {user_prefs['target_energy']}")
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


def main() -> None:
    songs = load_songs("data/songs.csv")

    for label, prefs in ALL_PROFILES:
        print_recommendations(label, prefs, songs, k=5)


if __name__ == "__main__":
    main()
