"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()

    # Define regular user preference profiles
    regular_profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.4
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.9
        }
    }

    # Define adversarial and edge case user profiles
    edge_case_profiles = {
        "Impossible Combo": {
            # No song has both rock + chill (rock is intense, lofi is chill)
            "genre": "rock",
            "mood": "chill",
            "energy": 0.5
        },
        "Extreme High Energy": {
            # Maximum energy preference (1.0) - only metal/edm get close
            "genre": "pop",
            "mood": "happy",
            "energy": 1.0
        },
        "Extreme Low Energy": {
            # Minimum energy preference (0.0) - tests if near-zero energy songs win
            "genre": "pop",
            "mood": "happy",
            "energy": 0.0
        },
        "Zero Points Profile": {
            # Genre/mood don't exist in dataset - will get 0 points from matching
            "genre": "reggaeton",  # Not in dataset
            "mood": "ecstatic",     # Not in dataset
            "energy": 0.5
        },
        "Genre Only": {
            # Matches only genre (pop), no mood match - tests if 2.0 + energy is enough
            "genre": "pop",
            "mood": "melancholic",  # No pop songs are melancholic
            "energy": 0.82
        },
        "Energy Cliff Test": {
            # Tests if a genre/mood match trumps terrible energy mismatch
            # User wants high energy folk (folk is always 0.25-0.45 energy)
            "genre": "folk",
            "mood": "sad",
            "energy": 0.95  # Huge mismatch with folk's low energy
        },
        "All Zeros": {
            # Technically valid but meaningless
            "genre": "pop",
            "mood": "happy",
            "energy": 0.5
        }
    }

    # Test regular profiles
    print("\n" + "="*60)
    print("REGULAR USER PROFILES")
    print("="*60)
    for profile_name, user_prefs in regular_profiles.items():
        print(f"\n{profile_name}:")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print("\nTop recommendations:\n")
        for rec in recommendations:
            song, score, explanation = rec
            print(f"  {song['title']} - Score: {score:.2f}")
            print(f"  Because: {explanation}")

    # Test edge case profiles
    print("\n" + "="*60)
    print("EDGE CASE & ADVERSARIAL PROFILES")
    print("="*60)
    for profile_name, user_prefs in edge_case_profiles.items():
        print(f"\n{'='*60}")
        print(f"EDGE CASE: {profile_name}")
        print(f"Preferences: {user_prefs}")
        print(f"{'='*60}")
        
        recommendations = recommend_songs(user_prefs, songs, k=3)
        
        print("\nTop recommendations:\n")
        for rec in recommendations:
            song, score, explanation = rec
            print(f"  {song['title']} - Score: {score:.2f}")
            print(f"  By {song['artist']} ({song['genre']}, {song['mood']}, energy: {song['energy']})")
            print(f"  Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
