#API
import streamlit as st
from cleaning import clean_question
from model import predict

with st.form(key='my_form'):
    question = st.text_input('Enter your Stack Overflow question')
    submit = st.form_submit_button('Submit')
    verbose = st.checkbox('Verbose')
    # st.write('Press submit tostre have your name printed below')
    if submit:
        if (len(question) == 0):
            st.write(':red[Please enter a question to get tag suggestion]')
        else:    
            cleaned = clean_question(question, verbose=verbose)
            tags_predicted = predict(cleaned)
            st.write('**Suggested tags :**', tags_predicted)


