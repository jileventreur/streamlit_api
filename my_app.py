#API
import streamlit as st
from preprocessing import clean_question

with st.form(key='my_form'):
    question = st.text_input('Enter your Stack Overflow question')
    submit = st.form_submit_button('Submit')
    # st.write('Press submit to have your name printed below')

    if submit:
        cleaned = clean_question(question, verbose=True)
        st.write('cleaned question :')
        st.write(cleaned)

