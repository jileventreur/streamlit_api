
import os.path
from bs4 import BeautifulSoup
from unidecode import unidecode
import spacy
from spacy.symbols import ORTH
#ressources
from resources.filtered_tags_set import filtered_tags_set
import streamlit as st

# file too big to be store in git so we have to dl it during first execution from gdrive
stopwords_path = 'resources\stopwords.py'
if not os.path.isfile(stopwords_path):
    import gdown
    url = 'https://drive.google.com/uc?id=1BMJor8iX-3ZK0-uFhJ9y3i1k6wbtgWa4'
    gdown.download(url, stopwords_path, quiet=False)    
from resources.stopwords import stopwords

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

# #add tags as special cases
for tag in filtered_tags_set:
  special_case = [{ORTH:tag}]
  nlp.tokenizer.add_special_case(tag, special_case)

def _lemmatization(text,
                  allowed_postags=["NOUN", "ADJ", "VERB", "ADV", "PROPN"]):
    doc = nlp(text)
    new_text = []
    for token in doc:
        if str(token) in filtered_tags_set:
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
    res = unidecode(res)
    res = res.lower()
    return res

gverbose = False
def _verbose_write(txt: str) -> None:
    if gverbose:
        st.write(txt)

def clean_question(question:str, verbose=False) -> str:
    global gverbose
    gverbose = verbose
    question = _strip_text(question)
    _verbose_write('stripped question :')
    _verbose_write(question)
    question = _lemmatization(question)
    _verbose_write('lemmatized question :')
    _verbose_write(question)
    question = ' '.join([token for token in question.split(" ") if token not in stopwords])
    _verbose_write('filtered question :')
    _verbose_write(question)
    return question
