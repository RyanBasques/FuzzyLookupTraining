"""
Flask api to return closest celebrity/movie/character matches (by score out of 100).
"""

from flask import Flask
import pickle
from operator import itemgetter
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_kernels

app = Flask(__name__)

with open('./data/celebs.pickle', 'rb') as handle:
    actor_list = pickle.load(handle, encoding='UTF-8')
with open('./data/movies.pickle', 'rb') as handle:
    movie_list = pickle.load(handle, encoding='UTF-8')
with open('./data/characters.pickle', 'rb') as handle:
    character_dict = pickle.load(handle, encoding='UTF-8')

character_list = list(character_dict.keys())
all_entities = actor_list + movie_list + character_list
actors_len = len(actor_list)
movies_len = len(movie_list)
character_len = len(character_list)

vec = CountVectorizer(analyzer='char', ngram_range=(1, 3))
vec_trans = vec.fit_transform(all_entities)

@app.route('/<user_input>')
def getSimilarNames(user_input):

    sim_scores = pairwise_kernels(
                     vec_trans,
                     vec.transform([user_input]),
                     metric='cosine').flatten().tolist()
    
    actor_scores = sim_scores[:actors_len]
    movie_scores = sim_scores[actors_len:actors_len+movies_len]
    character_scores = sim_scores[actors_len+movies_len:]
    
    actor_dict = [{"type":"actor", "value":a, "similarity_score":s} for a, s in zip(actor_list, actor_scores)]
    movie_dict = [{"type":"movie", "value":m, "similarity_score":s} for m, s in zip(movie_list, movie_scores)]

    actor_character_dict = []
    for character, score in zip(character_list,character_scores):
        for actor in character_dict[character]:
            actor_character_dict.append({"type":"actor", "value":actor, "similarity_score":score})
    
    all_dict = actor_dict + movie_dict + actor_character_dict
    all_dict_sorted = sorted(all_dict, key=itemgetter('similarity_score'), reverse=True)[:100]
    
    return json.dumps(all_dict_sorted, ensure_ascii=False).encode('utf8')

if __name__ == '__main__':
    app.run(debug=True)
