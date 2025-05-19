import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.title("📺 YouTube Niche Trend Analyzer")

# get data
try:
    videos = pd.read_csv("data/videos.csv")
    comments = pd.read_csv("data/comments_analyzed.csv")
except FileNotFoundError:
    st.error("Required data files not found. Please run the data collection scripts first.")
    st.stop()

# calculate avg sentiment for video/avg per video
avg_sentiment = comments.groupby("video_id")["sentiment"].mean().reset_index()
df = videos.merge(avg_sentiment, on="video_id")

def parse_view_count(view_str):
    """convert yt view strings like '2.5M' to integers."""
    if isinstance(view_str, str):
        view_str = view_str.replace(",", "").strip()
        match = re.match(r"([\d\.]+)([KMB]?)", view_str, re.IGNORECASE)
        if match:
            number = float(match.group(1))
            suffix = match.group(2).upper()
            if suffix == "B":
                return int(number * 1_000_000_000)
            elif suffix == "M":
                return int(number * 1_000_000)
            elif suffix == "K":
                return int(number * 1_000)
            else:
                return int(number)
    return 0

df["views"] = df["views"].apply(parse_view_count)

# scatter plot, views vs. sentiment
fig = px.scatter(
    df,
    x="views",
    y="sentiment",
    hover_data=["title", "channel"],
    title="Sentiment vs. Views"
)
st.plotly_chart(fig)

# list video with link
st.subheader("Video List")
for _, row in df.iterrows():
    st.markdown(f"[{row['title']}]({row['link']}) — {row['channel']}")

# positive comments with titles
comments_with_titles = comments.merge(videos[["video_id", "title", "link"]], on="video_id", how="left")
top_comments = comments_with_titles.sort_values(by="sentiment", ascending=False).head(10)
st.subheader("Top Positive Comments")
for _, row in top_comments.iterrows():
    st.markdown(f"- **[{row['title']}]({row['link']})**: {row['comment']}")
