from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Parse a songs CSV file and return a list of typed song dictionaries."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Score one song against a user profile (max 7.0) and return the score with a reason string."""
    score = 0.0
    reasons = []

    # --- Categorical ---
    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    if song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"mood match (+1.0)")

    # --- Numerical helpers ---
    TEMPO_MIN, TEMPO_MAX = 55.0, 158.0

    def num_score(song_val: float, target: float, weight: float, label: str) -> float:
        """Return weighted inverted-deviation points for a normalized [0,1] feature."""
        points = weight * (1.0 - abs(song_val - target))
        reasons.append(f"{label}: {song_val:.2f} vs target {target:.2f} (+{points:.2f})")
        return points

    def tempo_score(song_bpm: float, target_bpm: float, weight: float) -> float:
        """Normalize both BPM values to [0,1] before scoring to match the other feature scales."""
        song_norm   = (song_bpm   - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
        target_norm = (target_bpm - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
        points = weight * (1.0 - abs(song_norm - target_norm))
        reasons.append(f"tempo_bpm: {song_bpm:.0f} vs target {target_bpm:.0f} (+{points:.2f})")
        return points

    score += num_score(song["energy"],        user_prefs.get("target_energy",        0.5), 1.50, "energy")
    score += num_score(song["acousticness"],  user_prefs.get("target_acousticness",  0.5), 1.00, "acousticness")
    score += tempo_score(song["tempo_bpm"],   user_prefs.get("target_tempo_bpm",     100), 0.75)
    score += num_score(song["valence"],       user_prefs.get("target_valence",       0.5), 0.50, "valence")
    score += num_score(song["danceability"],  user_prefs.get("target_danceability",  0.5), 0.25, "danceability")

    explanation = " | ".join(reasons)
    return round(score, 4), explanation


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top-k with artist diversity enforced."""
    # Score every song
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)

    # Apply artist diversity cap
    results: List[Tuple[Dict, float, str]] = []
    artist_counts: Dict[str, int] = {}
    for song, score, explanation in scored:
        artist = song["artist"]
        if artist_counts.get(artist, 0) < 2:
            results.append((song, score, explanation))
            artist_counts[artist] = artist_counts.get(artist, 0) + 1
        if len(results) == k:
            break

    return results
