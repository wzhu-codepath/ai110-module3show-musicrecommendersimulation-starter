"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- recommend_songs
- ScoringStrategy classes (EnergyFocusedStrategy, GenreFirstStrategy, MoodFirstStrategy, BalancedStrategy)
"""

from recommender import (
	load_songs, 
	recommend_songs,
	EnergyFocusedStrategy,
	GenreFirstStrategy,
	MoodFirstStrategy,
	BalancedStrategy
)

try:
	from tabulate import tabulate
	HAS_TABULATE = True
except ImportError:
	HAS_TABULATE = False


def print_recommendations_table(recommendations, title="Recommendations"):
	"""
	Display recommendations in a formatted table using tabulate.
	
	Args:
		recommendations: List of (song, score, explanation) tuples
		title: Title for the table
	"""
	if not recommendations:
		print("No recommendations found.")
		return
	
	# Prepare table data
	table_data = []
	for i, rec in enumerate(recommendations, 1):
		song, score, explanation = rec
		table_data.append([
			i,
			song['title'],
			song['artist'],
			song['genre'],
			f"{score:.2f}",
			explanation
		])
	
	headers = ["#", "Title", "Artist", "Genre", "Score", "Reason"]
	
	print(f"\n{title}")
	print(tabulate(table_data, headers=headers, tablefmt="grid"))



def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    # Available scoring strategies
    strategies = [
        EnergyFocusedStrategy(),
        GenreFirstStrategy(),
        MoodFirstStrategy(),
        BalancedStrategy()
    ]

    print("\n" + "="*70)
    print("MUSIC RECOMMENDER SIMULATION - MULTIPLE STRATEGIES")
    print("="*70)
    print(f"\nUser Profile: {user_prefs}")
    print(f"(Genre: {user_prefs['genre']}, Mood: {user_prefs['mood']}, Energy: {user_prefs['energy']})\n")

    # Test each strategy
    for strategy in strategies:
        print("\n" + "="*100)
        print(f"STRATEGY: {strategy.get_name()}")
        print("="*100)
        recommendations = recommend_songs(user_prefs, songs, k=5, strategy=strategy)

        print_recommendations_table(recommendations, f"Top 5 recommendations (without diversity penalty)")
        
        # Show same strategy WITH diversity penalty
        recommendations_diverse = recommend_songs(user_prefs, songs, k=5, strategy=strategy, use_diversity_penalty=True)
        print_recommendations_table(recommendations_diverse, f"Top 5 recommendations (WITH diversity penalty)")

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

    # Test regular profiles with different strategies
    print("\n\n" + "="*100)
    print("REGULAR USER PROFILES - TESTED WITH ALL STRATEGIES")
    print("="*100)
    
    for profile_name, user_prefs in regular_profiles.items():
        print(f"\n{'='*100}")
        print(f"Profile: {profile_name} | Preferences: {user_prefs}")
        print(f"{'='*100}")
        
        for strategy in strategies:
            recommendations = recommend_songs(user_prefs, songs, k=3, strategy=strategy)
            print_recommendations_table(recommendations, f"  [{strategy.get_name()}] Top 3")

    # Test edge case profiles
    print("\n\n" + "="*100)
    print("EDGE CASE & ADVERSARIAL PROFILES")
    print("="*100)
    
    # Test one edge case with all strategies for comparison
    test_edge_case = "Impossible Combo"
    user_prefs = edge_case_profiles[test_edge_case]
    
    print(f"\n{'='*100}")
    print(f"EDGE CASE: {test_edge_case}")
    print(f"Preferences: {user_prefs}")
    print(f"Challenge: No song has both rock + chill (rock is intense, lofi is chill)")
    print(f"{'='*100}\n")
    
    for strategy in strategies:
        recommendations = recommend_songs(user_prefs, songs, k=3, strategy=strategy)
        print_recommendations_table(recommendations, f"[{strategy.get_name()}] Top 3")


if __name__ == "__main__":
    main()
