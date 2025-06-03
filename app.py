import streamlit as st
from googleapiclient.discovery import build
from textblob import TextBlob
import pandas as pd

# Load API key from secrets
YOUTUBE_API_KEY = st.secrets["youtube"]["api_key"]

def get_youtube_comments(video_id, max_results=100):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    comments = []
    try:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            textFormat="plainText"
        ).execute()
        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
    except Exception as e:
        st.error(f"Error fetching comments: {e}")
    return comments

def analyze_sentiment(comments):
    sentiments = []
    for comment in comments:
        analysis = TextBlob(comment)
        polarity = analysis.sentiment.polarity
        if polarity > 0:
            sentiment = "Positive"
        elif polarity == 0:
            sentiment = "Neutral"
        else:
            sentiment = "Negative"
        sentiments.append({"comment": comment, "sentiment": sentiment, "polarity": polarity})
    return sentiments

st.title("YouTube Video Comment Sentiment Analyzer")

video_url = st.text_input("Enter YouTube video URL or Video ID:")

if video_url:
    # Extract video ID if full URL given
    if "youtube.com" in video_url or "youtu.be" in video_url:
        import re
        # Simple regex to extract video ID from URL
        video_id_search = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", video_url)
        video_id = video_id_search.group(1) if video_id_search else video_url
    else:
        video_id = video_url

    comments = get_youtube_comments(video_id)
    if comments:
        st.success(f"Fetched {len(comments)} comments!")

        results = analyze_sentiment(comments)
        df = pd.DataFrame(results)

        st.subheader("Sentiment Counts")
        st.bar_chart(df["sentiment"].value_counts())

        st.subheader("Sample Comments and Sentiment")
        st.dataframe(df.head(20))
    else:
        st.warning("No comments found or error fetching comments.")
