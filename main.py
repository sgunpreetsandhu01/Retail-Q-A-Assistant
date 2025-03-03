from langchain_helper import get_few_shot_db_chain

import streamlit as st

st.title("Retail Q&A Assistant 👔")

question = st.text_input("Question:")

if question:
    chain = get_few_shot_db_chain()
    res = chain.invoke(question)
    st.header("Answer:")
    st.write(res['result'])
