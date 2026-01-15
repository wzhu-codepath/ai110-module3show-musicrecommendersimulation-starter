# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

 1. VibeFinder
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

1. This is a classroom exploration system that generates song recommendations based on user preferences for genre and energy level. It assumes users have a defined musical taste and clear energy preference (calm vs. energetic). This is for learning purposes, not real users—to understand how algorithm design choices create filter bubbles.


---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.


1. The recommender scores each song on: matching your genre preference (+1.0 point), matching your energy level (+up to 3.0 points), and mood match (turned off). Energy is the big factor—it calculates how close the song's energy is to what you want, with closer matches scoring higher. All scores add up, songs are ranked, and you get the top k recommendations.

    Key change: Energy importance was doubled from the starter (1.5 to 3.0 max points) and mood was commented out entirely.

---

## 4. Data  

Describe the dataset the model uses.  


Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

1. The catalog has 20 songs with 17 genres represented (pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, edm, folk, hip-hop, reggae, metal, classical, country, soul, blues). No songs were added or removed. Each song has energy, tempo, mood, and other musical attributes. Missing: artist popularity, user history, seasonal preferences—anything about *who* the user is beyond their genre and energy preference.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

1. It works really well for users whose main priority is energy level. The high-energy weighting correctly separates gym songs (Gym Hero at 0.93 energy, Bass Drop Nights at 0.89) from chill songs (Library Rain at 0.35, Spacewalk Thoughts at 0.28). Genre matching still helps when energy aligns. The explanations ("Perfect energy match") make sense to users.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

  1. The recommender weights song energy (how intense/fast it is) very heavily—3x more important than genre. This creates a "trap" where users get locked into only high-energy or only low-energy songs. A user who likes pop music but prefers calm, relaxing songs won't see any upbeat pop songs—instead, they'll only get mellow lofi or ambient tracks. The system forces them into a narrow energy band and ignores their genre preference if energy doesn't align.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

  1. I tested three user profiles: a high-energy gym-goer, a low-energy lofi listener, and a pop fan who wanted calm music. 
    
    The gym-goer got solid high-energy recommendations (Gym Hero, Bass Drop Nights, Storm Runner), which matched expectations. The lofi listener correctly received chill, low-energy songs. However, the pop fan with low-energy preference got almost no pop songs—instead receiving ambient and lofi tracks. This confirmed the energy filter bubble problem described in limitations.

    What surprised me: The system treats completely different genres (metal vs. classical) as equivalent if they match energy, which feels wrong. I also noticed that removing the mood check eliminated any emotional context from recommendations, making results feel generic.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

1. I'd re-enable mood with lower weight (0.3-0.5 points), use the unused features like danceability and acousticness to add diversity, soften the energy penalty so songs outside the range aren't zeroed out completely, and add a "serendipity factor" that occasionally recommends something slightly different to break filter bubbles. Also test with user profiles that prioritize mood or danceability instead of just energy.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps

1. I learned that small weight changes (doubling energy) have huge consequences on what users see. It's wild how the system "silently fails" for users outside the intended profile without any error message. The mood removal was surprising—recommendations felt generic without emotional context. This totally changed how I think about recommendations; they're not mathematical, they're *human*. Good ones need multiple overlapping signals.  
