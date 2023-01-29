import csv
import json


# NLP package imports
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


# sentence similarity setup
model_name = 'sentence-transformers/all-MiniLM-L6-v2'
sentence_comparer = SentenceTransformer(model_name)


# faq file setup
with open('./option2/solution/data/hackathon_FAQ.csv', 'r') as faq_file:
    faq_data = list(csv.reader(faq_file, delimiter=","))


# juding schedule setup
# judging_schedule.json data was taken from option1 coding challenges
with open('./option2/solution/data/judging_schedule.json', 'r') as json_file:
    judging_schedule = json.load(json_file)


# teams list file setup
with open('./option2/solution/data/teams_list.csv', 'r') as teams_file:
    teams_list = list(csv.reader(teams_file, delimiter=","))[0]