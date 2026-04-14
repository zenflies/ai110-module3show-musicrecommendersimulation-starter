# Reflection: Comparing Profile Outputs

Short notes on what changed between profiles and why it makes sense.

---

## High-Energy Pop vs. Chill Lofi

The Pop profile pushed the top results toward fast, loud, danceable tracks like "Gym Hero" and "Electric Feel."
The Lofi profile pulled in slow, quiet songs like "Focus Flow" and "Library Rain."
This makes sense — energy weight is the strongest numerical signal (1.5 pts), so flipping energy from 0.92 to 0.40 reshapes the entire ranking.
The genre bonus also matters: "lofi" songs cluster at low energy naturally, so both the genre match and the energy target agree with each other for the Lofi user.

---

## Chill Lofi vs. Deep Intense Rock

The Lofi profile returns soft, acoustic tracks. The Rock profile returns heavy, fast songs like "Peak Performance" and "Trail Blazer."
What's interesting is that the Rock profile asks for `mood: angry`, but no song in the dataset has that label.
So the Rock user never gets the +1.0 mood bonus — they're always scoring at most 6.0 out of 7.0.
The Lofi user asks for `mood: focused`, which does exist in the dataset, so they can reach the full 7.0.
That's a hidden disadvantage for the Rock user that has nothing to do with music fit.

---

## High-Energy Pop vs. Deep Intense Rock

Both want high energy (0.92 vs 0.88), so their top songs are similarly fast and loud.
The big difference is valence: Pop wants bright, happy-sounding songs (0.85), Rock wants dark, heavy ones (0.20).
Songs like "Storm Runner" score well for Rock because of low valence, but score poorly for Pop.
Songs like "Gym Hero" score well for Pop because of high valence, but lose points for Rock.
This shows the valence feature is doing real work to separate these two profiles even when energy is similar.

---

## [EDGE] Contradictory Sad Hype vs. High-Energy Pop

Both want high energy. The Sad Hype profile also wants very low valence (0.10) and `mood: sad`.
The Pop profile returns cheerful, upbeat songs. The Sad Hype profile also returns fast songs — but the valence penalty filters out the cheerful ones.
The top results for Sad Hype end up being intense rock/synthwave tracks with low valence, not pop.
This is actually a reasonable outcome for the numbers, but it feels wrong — a "sad but energetic" user probably doesn't want to be sent to rock when they asked for pop.
The genre bonus is wasted because no pop song has low enough valence to compete.

---

## [EDGE] Neutral No Preference vs. any named profile

The Neutral profile gets no genre or mood bonus (both are empty strings).
Every song's score is driven entirely by how close its numerics are to 0.5.
The scores all cluster in a narrow band — maybe 3.0 to 3.5 — and the rankings feel almost random.
Compare that to the Lofi profile, where the genre match alone adds 2.0 pts and clearly separates lofi songs from everything else.
This shows how important the categorical bonuses are. Without them, the system has very little signal to work with.

---

## [EDGE] Acoustic Rocker vs. Deep Intense Rock

Both ask for rock. Deep Intense Rock wants low acousticness (0.08), which matches real rock songs perfectly.
Acoustic Rocker wants very high acousticness (0.95), which almost no rock song in the dataset has.
Yet both profiles still get rock songs at the top, because the genre bonus (+2.0) is strong enough to keep rock songs in the lead even when acousticness is a terrible fit.
This reveals a bias: genre match can mask a poor feature match. An acoustic folk song would actually suit the Acoustic Rocker better, but it never shows up because its genre doesn't match.

---

## [EDGE] Boundary BPM vs. High-Energy Pop

Both are high-energy pop profiles. Boundary BPM pushes the tempo target to 158 BPM (the maximum in the normalisation range).
Most songs top out around 144–158 BPM, so the top results are basically the same fast tracks.
No scores went negative or above 7.0, which confirms the tempo normalisation is stable at the boundary.
The small insight here is that pushing to 158 BPM doesn't give you dramatically different results from targeting 145 BPM — the difference in normalized tempo is small, so it barely changes the ranking.
