# import libraries
import streamlit as st
from streamlit_player import st_player
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
import re
import pandas as pd
from readability import Readability
from PIL import Image

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

# set up title
st.title("Flesch-Kincaid Readability Test")
st.write('\n')

# calculate single text
st.header('Flesch Kincaid Calculator')

# input text
TextBox = st.text_area('Enter text to check the readability', height=200)

# run the test
test = st.button("Calculate Readability")

new_content = ''
new_string = TextBox.replace("\\n", "")
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
new_content = new_string14
    
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

