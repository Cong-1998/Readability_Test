# import libraries
import streamlit as st
from streamlit_player import st_player
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
import re
import pandas as pd
from PIL import Image
from en_readability import Readability
from ms_readability import Readability as ms_read


def cleaning(text):
    new_string = text.replace("\\n", "")
    new_string2 = new_string.replace("\\xa0", "")
    new_string3 = new_string2.replace("\\'", "")
    new_string4 = re.sub(r'www\S+', '', new_string3)
    new_string5 = new_string4.replace("Â", "")
    new_string6 = new_string5.replace("\\x9d", "")
    new_string7 = new_string6.replace("â€", "")
    new_string8 = new_string7.replace("â€œ", "")
    new_string9 = new_string8.replace("œ", "")
    new_string11 = re.sub(' +', ' ', new_string9).strip()
    new_string12 = new_string11.replace(". . .", "")
    new_string13 = re.sub(r'http\S+', '', new_string12)
    new_string14 = re.sub(r'[-+]?\d*\.\d+|\d+', '', new_string13)
    new_string15 = new_string14.replace('"', '')
    return new_string15

def tabs(default_tabs = [], default_active_tab=0):
    if not default_tabs:
        return None
    active_tab = st.radio("", default_tabs, index=default_active_tab)
    child = default_tabs.index(active_tab)+1
    st.markdown("""  
        <style type="text/css">
        div[role=radiogroup] > label > div:first-of-type {
            display: none
        }
        div[role=radiogroup] {
            flex-direction: unset
        }
        div[role=radiogroup] label {             
            border: 1px solid #999;
            background: #EEE;
            padding: 8px 24px;
            border-radius: 4px 4px 0 0;
            position: relative;
            top: 1px;
            }
        div[role=radiogroup] label:nth-child(""" + str(child) + """) {    
            background: #FFF !important;
            border-bottom: 1px solid transparent;
        }            
        </style>
    """,unsafe_allow_html=True)        
    return active_tab

# hide menu bar
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# set up layout
padding = 1
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

# set up tab
active_tab = tabs(["Flesch-Kincaid", "Khadijah-Rohani"])

if active_tab == "Flesch-Kincaid":
    # set up title
    st.markdown("<h1 style='text-align: center;'>Flesch-Kincaid Readability Test</h1>", unsafe_allow_html=True)
    st.write('\n')
    
    # calculate single text
    st.header('Flesch Kincaid Calculator')
    
    # input text
    TextBox = st.text_area('Enter text to check the readability', height=200)

    # run the test
    test = st.button("Calculate Readability")

    new_content = cleaning(TextBox)
    
    if test:
        my_expander = st.expander(label='Cleaned Text')
        with my_expander:
            st.write(new_content)
        r = Readability(new_content)
        fk = r.flesch_kincaid()
        statis = r.statistics()
        word = list(statis.items())[1][1]
        sentence = list(statis.items())[2][1]
        syllable = r.syll_count()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Flesh-Kincaid Score", round(fk.score, 1))
        col2.metric("Total of Words", word)
        col3.metric("Total of Sentences", sentence)
        col4.metric("Total Syllables", syllable)
    st.write('\n')
    
    
elif active_tab == "Khadijah-Rohani":
    # set up title
    st.markdown("<h1 style='text-align: center;'>Ujian Kebolehbacaan Khadijah-Rohani</h1>", unsafe_allow_html=True)
    st.write('\n')

    # calculate single text
    st.header('Khadijah Rohani Calculator')

    # checkbox
    agree = st.checkbox('Used Augmented Formula')

    if agree:
        st.write("The augmented formula is not constrained by word count, but it is not the official formula.")
        st.write("\n")
        TextBox3 = st.text_area('Enter text to check the readability', height=200)
        test3 = st.button("Calculate Readability")
        new_content3 = cleaning(TextBox3)
        if test3:
            my_expander = st.expander(label='Cleaned Text')
            with my_expander:
                st.write(new_content3)
            r = ms_read(new_content3)
            statis = r.statistics()
            word = list(statis.items())[0][1]
            sentence = list(statis.items())[1][1]
            syllable = list(statis.items())[2][1]

            score = (0.3793*word/sentence)+(0.0207*syllable*300/word)-13.988

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Khadijah Rohani Score", round(score, 1))
            col2.metric("Total of Words", word)
            col3.metric("Total of Sentences", sentence)
            col4.metric("Total Syllables", syllable)
        st.write('\n')

    else:
        # input text
        TextBox2 = st.text_area('Enter text to check the readability', height=200)

        # run the test
        test2 = st.button("Calculate Readability")

        new_content2 = cleaning(TextBox2)

        if test2:
            my_expander = st.expander(label='Cleaned Text')
            with my_expander:
                st.write(new_content2)
            r = ms_read(new_content2)
            kr = r.khadijah_rohani()
            statis = r.statistics()
            word = list(statis.items())[0][1]
            sentence = list(statis.items())[1][1]
            syllable = list(statis.items())[2][1]

            if word < 300 or word > 300:
                st.error("300 words required.")

            else:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Khadijah Rohani Score", round(kr.score, 1))
                col2.metric("Total of Words", word)
                col3.metric("Total of Sentences", sentence)
                col4.metric("Total Syllables", syllable)
        st.write('\n')

else:
    st.error("Something has gone wrong.")
