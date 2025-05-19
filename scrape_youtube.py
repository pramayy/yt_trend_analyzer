from youtubesearchpython import VideosSearch
import pandas as pd
from googleapiclient.discovery import build
import os

# checking if data diary exists
os.makedirs("data", exist_ok=True)

# API key for yt 
API_KEY = 'AIzaSyAEiWO9hDckAHevf-WC7r0efzMDXY_HBt8'  # Please add your own API Key here
youtube = build('youtube', 'v3', developerKey=API_KEY)

def search_videos(query, limit=20):
    """
    search for yt videos
    according to keywords
    return data 
    """
    videos_search = VideosSearch(query, limit=limit)
    results = videos_search.result().get('result', [])
    data = []
    for v in results:
        try:
            data.append({
                'title': v['title'],
                'channel': v['channel']['name'],
                'views': v['viewCount']['short'],
                'duration': v['duration'],
                'link': v['link'],
                'video_id': v['id']
            })
        except KeyError:
            continue
    return pd.DataFrame(data)

def fetch_comments(video_id):
    """
    get comments from the videos
    """
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=50,
            textFormat="plainText"
        )
        response = request.execute()
        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
    except Exception as e:
        print(f"Error fetching comments for {video_id}: {e}")
    return comments

if __name__ == "__main__":
    print("Welcome to the YouTube Trend Analyzer!")
    query = input("Enter keywords to search on YouTube: ").strip()
    if not query:
        print("No keywords entered. Exiting.")
        exit()

    print(f"Searching for videos about: {query}")
    df = search_videos(query, limit=10)
    if df.empty:
        print("No videos found for your query.")
        exit()
    df.to_csv("data/videos.csv", index=False)
    print(f"Saved {len(df)} videos to data/videos.csv.")

    all_comments = []
    print("Fetching comments for each video...")
    for vid in df["video_id"]:
        comments = fetch_comments(vid)
        for comment in comments:
            all_comments.append({'video_id': vid, 'comment': comment})

    pd.DataFrame(all_comments).to_csv("data/comments.csv", index=False)
    print(f"Saved {len(all_comments)} comments to data/comments.csv.")

    print("\nSample of collected videos:")
    print(df[["title", "channel", "views"]].head())
