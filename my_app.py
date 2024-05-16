import streamlit as st

st.write('Hello, *World!* :sunglasses:')

# Using the "with" syntax
with st.form(key='my_form'):
    name = st.text_input('Enter your name')
    submit = st.form_submit_button('Submit')
    st.write('Press submit to have your name printed below')

    if submit:
        st.write(f'hello {name}')