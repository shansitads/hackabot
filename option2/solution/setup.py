import csv

# NLP package imports
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# sentence similarity setup
model_name = 'sentence-transformers/all-MiniLM-L6-v2'
sentence_comparer = SentenceTransformer(model_name)

# faq file setup
faq_file = open('./data/hackathonFAQ.csv','r')
faq_data = list(csv.reader(faq_file, delimiter=","))
faq_file.close