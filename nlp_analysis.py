import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from textblob import TextBlob
import os

# check for data file
if not os.path.exists("data/comments.csv"):
    print("Missing comments.csv. Please run scrape_youtube.py first to collect comments.")
    exit()

def analyze_sentiment(comment):
    """get sentiment score with textblob"""
    return TextBlob(comment).sentiment.polarity

def extract_topics(comments, n_topics=5):
    """
    Extracts main topics from a list of comments using TF-IDF and NMF.
    Returns a list of topic keywords.
    """
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=1, stop_words='english')
    tfidf = vectorizer.fit_transform(comments)
    nmf = NMF(n_components=n_topics, random_state=42)
    W = nmf.fit_transform(tfidf)
    H = nmf.components_
    feature_names = vectorizer.get_feature_names_out()

    topics = []
    for topic_idx, topic in enumerate(H):
        # getting top 5 words
        top_words = [feature_names[i] for i in topic.argsort()[:-6:-1]]
        topics.append(" ".join(top_words))
    return topics

if __name__ == "__main__":
    # use comments and analyze sentiments
    df = pd.read_csv("data/comments.csv")
    df = df.dropna(subset=["comment"])
    df["sentiment"] = df["comment"].apply(analyze_sentiment)
    print(df.head())
    print(df.columns)
    df.to_csv("data/comments_analyzed.csv", index=False)
    print("Sentiment analysis complete. Results saved to data/comments_analyzed.csv.")

    # extract and show topics
    topics = extract_topics(df["comment"])
    print("\nTop Discussion Topics in Comments:")
    for idx, t in enumerate(topics, 1):
        print(f"Topic {idx}: {t}")





