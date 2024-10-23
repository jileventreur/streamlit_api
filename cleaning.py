
import os.path
from bs4 import BeautifulSoup
from unidecode import unidecode
import spacy
from spacy.symbols import ORTH
#ressources
# from resources.filtered_tags_set import filtered_tags_set
import streamlit as st
import pickle

# # file too big to be store in git so we have to dl it during first execution from gdrive
# stopwords_path = 'resources\stopwords.py'
# if not os.path.isfile(stopwords_path):
#     import gdown
#     url = 'https://drive.google.com/uc?id=1BMJor8iX-3ZK0-uFhJ9y3i1k6wbtgWa4'
#     gdown.download(url, stopwords_path, quiet=False)    
# from resources.stopwords import stopwords

g_verbose = False

#init global variable
_nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
with open('resources/tags.pkl', 'rb') as file:
  tags = pickle.load(file)
with open('resources/vocabulary.pkl', 'rb') as file:
  vocabulary = pickle.load(file)
  vocabulary |= tags

# #add tags as special cases in tokenizer
for tag in tags:
  special_case = [{ORTH:tag}]
  _nlp.tokenizer.add_special_case(tag, special_case)

def _lemmatization(text,
                  allowed_postags=["NOUN", "ADJ", "VERB", "ADV", "PROPN"]):
    doc = _nlp(text)
    new_text = []
    for token in doc:
        if str(token) in tags:
            new_text.append(str(token))
        elif token.pos_ in allowed_postags :
            new_text.append(token.lemma_)
    res = " ".join(new_text)
    return res

def _strip_text(txt:str) -> str:
    soup = BeautifulSoup(txt, "lxml")
    for s in soup.select('code'):
        s.extract()
    res = soup.text
    res = res.replace('\n', ' ')
    res = res.replace('\\n', ' ')
    res = unidecode(res)
    res = res.lower()
    return res

def _verbose_write(headline: str, question: str) -> None:
    if g_verbose:
        st.write(f'**{headline}**')
        st.code(question)

def clean_question(question:str, verbose=False) -> str:
    global g_verbose
    g_verbose = verbose
    _verbose_write('Input :', question)
    question = _strip_text(question)
    _verbose_write('Stripped question :', question)
    question = _lemmatization(question)
    _verbose_write('Lemmatized question :', question)
    question = ' '.join([token for token in question.split(' ') if token in vocabulary])
    _verbose_write('Word filtered question :', question)
    if verbose: 
       st.divider()
    return question
