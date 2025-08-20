import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI as Google
import os
from langchain import PromptTemplate, LLMChain

st.set_page_config(page_title='Tweet Generator', page_icon='🪺', layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Tweet Generator")

os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']
model = Google(model = "gemini-1.5-flash-latest")

tweet_template = """
Give me {number} tweets on {topic} in {language}.
Please follow the below instructions:
1. Do not translate to English if the given language is not English.
2. If {language} is empty or not a real language, default to English and ignore {language}.
3. If {topic} is empty or does not make sense, then respond with "Please enter a topic for your tweet!".
4. Avoid unnecessary indents or spaces.
5. Keep the tweets short, but include at least 1 hashtag per tweet.
"""
tweet_prompt = PromptTemplate(template = tweet_template, input_variables = ['number', 'topic', 'language'])

with st.form(key = 'tweets'):
    topic = st.text_input("Topic: ")
    number = st.number_input("Number of Tweets: ", value = 1, step = 1, max_value = 10, min_value = 1)
    language = st.text_input("Language: ")
    submit = st.form_submit_button("Generate")

if submit:
    tweet_chain = tweet_prompt | model
    response = tweet_chain.invoke({"number": number,
                                   "topic": topic,
                                   "language": language,})
    st.write(response.content)
