import csv

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

def score_song(song, user_prefs):
	"""
	Score a song based on user preferences using our algorithm recipe:
	- Genre Match: +2.0 points
	- Mood Match: +1.0 point
	- Energy Similarity: +0 to 1.5 points
	Returns a numerical score.
	"""
	score = 0.0
	
	# Genre match: +1.0
	if song['genre'] == user_prefs['genre']:
		score += 1.0
	
	# Mood match: +1.0
	# if song['mood'] == user_prefs['mood']:
	# 	score += 1.0
	
	# Energy similarity: +0 to 3.0
	energy_diff = abs(song['energy'] - user_prefs['energy'])
	energy_score = max(0, 3.0 - (energy_diff * 3.0))
	score += energy_score
	
	return score


def recommend_songs(user_prefs, songs, k):
	"""
	Score all songs and return top k recommendations sorted by score (highest first).
	Returns list of tuples: (song, score, explanation)
	"""
	def get_explanation(song, score):
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
	
	scored_songs = [
		(song, score_song(song, user_prefs), get_explanation(song, score_song(song, user_prefs)))
		for song in songs
	]
	# Sort by score (index 1) in descending order, return top k
	return sorted(scored_songs, key=lambda x: x[1], reverse=True)[:k]