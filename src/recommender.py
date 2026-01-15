import csv
from abc import ABC, abstractmethod


def load_songs(filename):
	"""
	Reads a CSV file of songs and returns a list of dictionaries.
	Converts numerical fields to float or int for later math operations.
	"""
	songs = []
	with open(filename, newline='', encoding='utf-8') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			song = {
				'id': int(row['id']),
				'title': row['title'],
				'artist': row['artist'],
				'genre': row['genre'],
				'mood': row['mood'],
				'energy': float(row['energy']),
				'tempo_bpm': int(row['tempo_bpm']),
				'valence': float(row['valence']),
				'danceability': float(row['danceability']),
				'acousticness': float(row['acousticness'])
			}
			songs.append(song)
	print(f"Loaded songs: {len(songs)}")
	return songs


class ScoringStrategy(ABC):
	"""Abstract base class for different scoring strategies."""
	
	@abstractmethod
	def score_song(self, song, user_prefs):
		"""Score a song based on user preferences."""
		pass
	
	@abstractmethod
	def get_name(self):
		"""Return the name of this strategy."""
		pass


class EnergyFocusedStrategy(ScoringStrategy):
	"""Prioritizes energy matching (current implementation)."""
	
	def score_song(self, song, user_prefs):
		"""
		Score: Energy heavily weighted (+0 to 3.0), genre match (+1.0), mood disabled
		"""
		score = 0.0
		
		# Genre match: +1.0
		if song['genre'] == user_prefs['genre']:
			score += 1.0
		
		# Energy similarity: +0 to 3.0
		energy_diff = abs(song['energy'] - user_prefs['energy'])
		energy_score = max(0, 3.0 - (energy_diff * 3.0))
		score += energy_score
		
		return score
	
	def get_name(self):
		return "Energy-Focused"


class GenreFirstStrategy(ScoringStrategy):
	"""Prioritizes genre matching above all else."""
	
	def score_song(self, song, user_prefs):
		"""
		Score: Genre match (+3.0), mood match (+1.0), energy similarity (+0 to 1.0)
		"""
		score = 0.0
		
		# Genre match: +3.0 (highest priority)
		if song['genre'] == user_prefs['genre']:
			score += 3.0
		
		# Mood match: +1.0
		if song['mood'] == user_prefs['mood']:
			score += 1.0
		
		# Energy similarity: +0 to 1.0 (lower importance)
		energy_diff = abs(song['energy'] - user_prefs['energy'])
		energy_score = max(0, 1.0 - (energy_diff * 1.0))
		score += energy_score
		
		return score
	
	def get_name(self):
		return "Genre-First"


class MoodFirstStrategy(ScoringStrategy):
	"""Prioritizes mood and emotional context."""
	
	def score_song(self, song, user_prefs):
		"""
		Score: Mood match (+2.5), energy similarity (+0 to 2.0), genre match (+1.0)
		"""
		score = 0.0
		
		# Mood match: +2.5 (highest priority)
		if song['mood'] == user_prefs['mood']:
			score += 2.5
		
		# Energy similarity: +0 to 2.0
		energy_diff = abs(song['energy'] - user_prefs['energy'])
		energy_score = max(0, 2.0 - (energy_diff * 2.0))
		score += energy_score
		
		# Genre match: +1.0
		if song['genre'] == user_prefs['genre']:
			score += 1.0
		
		return score
	
	def get_name(self):
		return "Mood-First"


class BalancedStrategy(ScoringStrategy):
	"""Equally weights all three factors."""
	
	def score_song(self, song, user_prefs):
		"""
		Score: Genre match (+1.0), mood match (+1.0), energy similarity (+0 to 1.0)
		All weighted equally.
		"""
		score = 0.0
		
		# Genre match: +1.0
		if song['genre'] == user_prefs['genre']:
			score += 1.0
		
		# Mood match: +1.0
		if song['mood'] == user_prefs['mood']:
			score += 1.0
		
		# Energy similarity: +0 to 1.0
		energy_diff = abs(song['energy'] - user_prefs['energy'])
		energy_score = max(0, 1.0 - (energy_diff * 1.0))
		score += energy_score
		
		return score
	
	def get_name(self):
		return "Balanced"


def score_song(song, user_prefs, strategy=None):
	
	"""
	Score a song based on user preferences using the specified strategy.
	Defaults to Energy-Focused if no strategy provided.
	"""
	if strategy is None:
		strategy = EnergyFocusedStrategy()
	return strategy.score_song(song, user_prefs)


def recommend_songs(user_prefs, songs, k, strategy=None, use_diversity_penalty=False):
	"""
	Score all songs and return top k recommendations sorted by score (highest first).
	Returns list of tuples: (song, score, explanation)
	
	Args:
		user_prefs: User preference dictionary
		songs: List of song dictionaries
		k: Number of recommendations to return
		strategy: ScoringStrategy instance (defaults to EnergyFocusedStrategy)
		use_diversity_penalty: If True, penalize songs from artists/genres already in recommendations
	"""
	if strategy is None:
		strategy = EnergyFocusedStrategy()
	
	def get_explanation(song, score, penalty_applied=False):
		"""Generate explanation for this recommendation."""
		reasons = []
		
		if song['genre'] == user_prefs['genre']:
			reasons.append(f"Matches your {song['genre']} preference")
		
		if song['mood'] == user_prefs['mood']:
			reasons.append(f"Has the {song['mood']} mood you want")
		
		energy_diff = abs(song['energy'] - user_prefs['energy'])
		if energy_diff < 0.2:
			reasons.append("Perfect energy match")
		elif energy_diff < 0.5:
			reasons.append("Close energy match")
	
		
		return " • ".join(reasons) if reasons else "Similar vibe"
	
	# First pass: score all songs
	scored_songs = [
		(song, strategy.score_song(song, user_prefs), False)
		for song in songs
	]
	
	# If diversity penalty is enabled, apply iterative selection
	if use_diversity_penalty:
		recommendations = []
		used_artists = set()
		used_genres = set()
		
		# Sort by initial score
		scored_songs_sorted = sorted(scored_songs, key=lambda x: x[1], reverse=True)
		
		# Greedily select songs, applying penalties
		for song, score, _ in scored_songs_sorted:
			if len(recommendations) >= k:
				break
			
			# Calculate diversity penalty
			penalty = 0.0
			penalty_applied = False
			
			# Penalize if artist already in recommendations
			if song['artist'] in used_artists:
				penalty -= 2.0  # Significant penalty for duplicate artists
				penalty_applied = True
			
			# Penalize if genre already appears twice in recommendations
			genre_count = sum(1 for rec_song, _, _ in recommendations if rec_song['genre'] == song['genre'])
			if genre_count >= 2:
				penalty -= 1.5  # Penalty for too many songs from same genre
				penalty_applied = True
			
			adjusted_score = score + penalty
			explanation = get_explanation(song, adjusted_score, penalty_applied)
			
			recommendations.append((song, adjusted_score, explanation))
			used_artists.add(song['artist'])
			used_genres.add(song['genre'])
		
		return recommendations
	else:
		# Original behavior: just sort by score
		scored_songs_with_explanations = [
			(song, score, get_explanation(song, score, False))
			for song, score, _ in scored_songs
		]
		return sorted(scored_songs_with_explanations, key=lambda x: x[1], reverse=True)[:k]