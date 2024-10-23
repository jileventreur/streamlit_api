#API
import streamlit as st
from cleaning import clean_question
from model import predict

with st.form(key='my_form'):
    question = st.text_input('Enter your Stack Overflow question')
    submit = st.form_submit_button('Submit')
    # st.write('Press submit tostre have your name printed below')
    if submit:
        cleaned = clean_question(question, verbose=False)
        # st.write('cleaned question :')
        # st.write(cleaned)
        tags_predicted = predict(cleaned)
        st.write(tags_predicted)


