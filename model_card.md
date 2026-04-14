# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder suggests songs that match how a user feels right now.
You tell it your preferred genre, mood, and targets for energy, tempo, acousticness, valence, and danceability.
It scores every song in the catalog against those preferences and returns the five best matches.
This is a classroom simulation — not a production app.

---

## 3. Algorithm Summary

Each song starts at zero points and earns points in two ways.

**Categorical bonuses (all-or-nothing):**
- Genre match: +2.0 points
- Mood match: +1.0 point

**Numeric closeness scores:**
Each numeric feature (energy, acousticness, tempo, valence, danceability) compares the song's value to the user's target. The closer the match, the more points — up to a per-feature cap.
Energy matters most (up to 1.5 pts). Danceability matters least (up to 0.25 pts).
Tempo is normalized to a 0–1 scale before scoring so it's comparable to the other features.

The maximum possible score is 7.0. After scoring all songs, the top 5 are returned, with no more than 2 songs from the same artist.

---

## 4. Data Used

- **Size:** 20 songs
- **Genres:** pop, lofi, rock, ambient, jazz, synthwave, indie pop (2–3 songs each)
- **Moods:** chill, focused, happy, intense, moody, relaxed
- **Features per song:** genre, mood, energy, tempo (BPM), valence, danceability, acousticness
- **Limits:** No real user listening history. No lyrics, key, or loudness data. The catalog is tiny — a real service has millions of songs.

---

## 5. Strengths

- Works well for users whose preferences align with the dataset vocabulary (e.g., asking for `lofi / focused` returns exactly the right quiet, slow tracks).
- The artist diversity cap (max 2 per artist) prevents one artist from flooding the top 5.
- Numeric scoring rewards close matches smoothly — a song that is slightly off still gets partial credit instead of being cut entirely.
- Stable at edge cases: empty genre/mood strings don't crash the system, and BPM targets at the normalisation boundary (158 BPM) produce valid scores.

---

## 6. Observed Behavior / Biases

**Mood label mismatch silently disqualifies many users.**
The dataset only uses six mood labels: `chill`, `focused`, `happy`, `intense`, `moody`, and `relaxed`.
Any user who requests `sad`, `angry`, or `energetic` can never earn the +1.0 mood bonus, because no song carries those labels.
This is invisible — the system doesn't warn the user; it just quietly scores lower.
A user asking for `mood: energetic` is penalized compared to an identical user asking for `mood: intense`, even though the music fit is the same.
A fix would be to map synonyms to canonical labels before scoring, or replace the all-or-nothing bonus with a soft similarity score.

---

## 7. Evaluation Process

Seven profiles were tested against the 20-song catalog.

| Profile | Type |
|---|---|
| High-Energy Pop | Standard |
| Chill Lofi | Standard |
| Deep Intense Rock | Standard |
| Contradictory Sad Hype (energy: 0.9, mood: sad) | Adversarial |
| Neutral / No Preference (all targets at 0.5) | Adversarial |
| Acoustic Rocker (rock genre, acousticness: 0.95) | Adversarial |
| Boundary BPM (target: 158 BPM) | Adversarial |

Each run was checked by reading the top-5 song list and asking: does this make sense for this user?

**Surprises:**
- The Sad Hype profile ignored its `sad` mood entirely and just returned the fastest songs — energy weight dominated.
- The Neutral profile clustered all scores in a narrow 3.0–3.5 band, making rankings feel almost random.
- The Acoustic Rocker profile kept returning standard rock songs despite a very poor acousticness fit, because the +2.0 genre bonus outweighed the penalty.
- Boundary BPM produced no crashes or out-of-range scores.

---

## 8. Intended Use and Non-Intended Use

**Intended use:**
A classroom exercise for understanding how feature-based scoring and weighting work in recommender systems.
Good for experimenting with how changing weights or user preferences shifts results.

**Not intended for:**
- Real music discovery — the catalog is too small and the scoring is too simple.
- Users with complex or conflicting tastes — the system has no way to represent "I like both calm jazz and heavy metal depending on the day."
- Any production deployment — there is no personalization, no feedback loop, and no handling of new or unknown songs.

---

## 9. Ideas for Improvement

1. **Mood synonym mapping.** Before scoring, translate common user moods (`sad`, `angry`, `energetic`) to the nearest dataset label. This would stop silently penalizing users whose vocabulary doesn't match the catalog.

2. **Reduce genre bonus dominance.** The +2.0 genre bonus can override poor feature matches (e.g., Acoustic Rocker getting non-acoustic rock). Lowering it to +1.0–1.5 and adding a soft genre similarity score would produce more honest rankings.

3. **User feedback loop.** Let the user rate the top result (thumbs up / down), then adjust the feature weights for the next query. Even one round of feedback would make the system feel much more personalized.

---

## 10. Personal Reflection

Building this showed how much a small weighting decision shapes the results.
Doubling the energy weight felt minor in code but completely changed which songs appeared at the top.
The most surprising thing was the mood mismatch bug — the system never complained, it just silently gave worse results to users who described their mood differently.
Real apps like Spotify probably face the same problem at a much larger scale, which is why they rely on listening history instead of asking users to describe themselves in words.
