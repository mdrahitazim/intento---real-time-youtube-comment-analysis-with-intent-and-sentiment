import streamlit as st
from pytube import extract
import pandas as pd
import fetch_comment
import detectTrans

# Set the Streamlit app layout to full width
st.set_page_config(layout="wide")
# Logo
st.image('logo.jpeg', width=200)
# Title of the Streamlit app
st.title('YouTube Comment Intent and Sentiment Analysis')

# Create a text input box for entering a search term
video_url = st.text_input('paste youtube link here')

if video_url:

    video_id = extract.video_id(video_url)

    # st.write(video_id)

    col1, col2 = st.columns(2)
        
    with col1:
        st.title('Your Video')
        st.video(video_url)
   
    with col2:
        st.title("Comments: ")
        df = pd.DataFrame()
        for i in [video_id]:
            df2 = fetch_comment.getcomments(i)
            df = pd.concat([df, df2])

        # showing all comments
        st.write(df.text)

    
    st.title("Sentiments: ")
    howmany = st.select_slider(label='how many top comments to analyze (by default 5 top comments will be analyzed)',options=[5,10,20,50,100])
    #showing only top [no of] comments
    df1 = df.sort_values(by=['like_count'], ascending=False).head(int(howmany))
    # st.write(df1)
    with st.spinner(f'Analyzing {howmany} comments...'):
        result_df1 = detectTrans.detect_translate_and_analyze(df1['text'])
        print(result_df1)
        st.write(result_df1)

        col1, col2 = st.columns(2)
            
        with col1:
            st.header('Sentiment Analysis')
            st.image('sentiment.png')
                
        with col2:
            st.header('Intent Analysis')
            st.image('intent.png')