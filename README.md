# 🎵 Music Recommender Simulation

## Project Summary

- Real AI recommenders, such as Spotify, use convolutional neural networks to breakdown the auditory components of user-selected songs, recommending similar music. This application takes a holistic approach, evaluating the aggregate data of both the music and user profile preferences to evalute a ranked-choice system for song recommendations. 

![Music System Architecture](music%20system.png)

---

## How The System Works

- Song classes will hold a variety of auditory component and metadata: artist, genre, mood, energy, tempo, valence, acousticness, and danceability
- A user profile will consist of a favorite song, mood, energy, and preferences for all song components
- The recommendation system calculates weights based on user preference and song content, providing explanations for each choice
- The algorithm uses hard filters, such as genre and mood, to ensure that users receive music that pertains to their taste. Additional numerical features are focused on zeroing in on inter-genre songs. 
- In this manner, there exist potential biases in favoring genre and mood, causing potentially favorable songs to be overlooked. 

![Terminal View](terminal.png)

---

## Edge Case Overview

![Edge Case Profiles](edge1.png)
![](edge2.png)
![](edge3.png)
![](edge4.png)

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

