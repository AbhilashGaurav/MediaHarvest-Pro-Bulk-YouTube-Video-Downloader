import streamlit as st
from googleapiclient.discovery import build
from pytube import YouTube
import os
import zipfile
import shutil
import json


# this is for session state to know whehter to have the json data after reload or not
if 'count' not in st.session_state:
    st.session_state.count = 0

# Increment a count variable on button click
# if st.button("Click me"):

# Display the current count
    # st.write(f"Count: {st.session_state.count}")
if st.session_state.count==0:
    file_name = "json_search_response.json"  # Replace with your file name
    empty_data = {}
        # Open the JSON file for reading
    with open(file_name, 'w') as file:
        json.dump(empty_data, file)

# Function to download YouTube video under a specified duration limit
def download_youtube_video(link, output_path, quality, duration_limit=None):
    try:
        yt = YouTube(link)
        duration = yt.length  # Duration in seconds
        if duration_limit is None or duration <= duration_limit:
            video = yt.streams.filter(res=quality).first()
            video.download(output_path)
            st.write(f"✅ Video '{yt.title}' ({quality}) received from the server Successfully")
            return True
        else:
            st.write(f"❌ Video '{yt.title}' has a duration of {duration} seconds and exceeds the {duration_limit} seconds limit.")
            return False
    except Exception as e:
        st.write(f"❌ Error occurred while downloading the video from: {link}")
        return False

# Set the title of the Streamlit app
st.title("YouTube Video Search and Downloader")

# Create an output folder to save the videos
output_folder = "downloaded_videos"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Create a list to store failed downloads
failed_downloads = []

# User input: Search query
search_query = st.text_input("Enter your YouTube search query:")

# YouTube Data API key (replace with your API key)
api_key = ""

# Initialize a list to store video data
all_fetched_links = []

# Initialize a list to store selected video URLs
selected_videos = []

search_response = {}

if st.button("Search"):
    try:
        if search_query:
            # Create a YouTube Data API client
            st.session_state.count += 1
            youtube = build("youtube", "v3", developerKey=api_key)

            # Perform the YouTube video search with 'part' parameter
            search_response = youtube.search().list(
                q=search_query,
                type="video",
                maxResults=15,  # Adjust the number of results as needed
                part="snippet"  # Include 'snippet' data in the response
            ).execute()
            # st.write(type(search_response))
            search_response_json= json.dumps(search_response)
            filename = "json_search_response.json"
            with open(filename, 'w') as json_file:
                json_file.write(search_response_json)
        else:
            st.warning("Please enter a search query.")
    except Exception as e:
        pass

# def store_results(search_response):
#     if search_response:
#         for search_result in search_response.get("items", []):
#             video_title = search_result["snippet"]["title"]
#             video_url = f'https://www.youtube.com/watch?v={search_result["id"]["videoId"]}'
#             thumbnail_url = search_result["snippet"]["thumbnails"]["default"]["url"]
#             all_fetched_links.append({"title": video_title, "url": video_url, "thumbnail": thumbnail_url})
#             # selected = st.checkbox(f"Select '{video_title}'", value=video_url in selected_videos)
#             # if selected:
#             #     selected_videos.append(video_url)
#             st.write(f"**Title:** {video_title}")
#             st.image(thumbnail_url)


def select_videos():

    file_name = "json_search_response.json"  # Replace with your file name

    # Open the JSON file for reading
    with open(file_name, 'r') as json_file:
        # Parse the JSON data into a Python dictionary
        data = json.load(json_file)
    
    col1, col2,col3 = st.columns(3)
    mark=1
    for item in data.get('items', []):
        video_url=f'https://www.youtube.com/watch?v={item["id"]["videoId"]}'
        video_title = item["snippet"]["title"]
        thumbnail=item["snippet"]["thumbnails"]["default"]["url"]
        a=('https://www.youtube.com/watch?v='+str(item["id"]["videoId"]))
        # st.write(f'<iframe width="560" height="315" src={a} frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
        if (len(video_title)>45):
            video_title=video_title[:45]+'...'
        if mark<=5:
            with col1:
                st.video(a)
                selected = st.checkbox(f"Select {video_title}")
                if selected:
                    selected_videos.append(video_url)
            mark+=1
        elif mark>5 and mark<=10:
            with col2:
                st.video(a)
                selected = st.checkbox(f"Select '{video_title}'")
                if selected:
                    selected_videos.append(video_url)
            mark+=1
        else:
            with col3:
                st.video(a)
                selected = st.checkbox(f"Select '{video_title}'")
                if selected:
                    selected_videos.append(video_url)


    if selected_videos:
        st.sidebar.subheader("Selected Videos:")
        for selected_video_url in selected_videos:
            st.sidebar.write(selected_video_url)

# # Provide a button to download the selected videos
# if selected_videos:
#     if st.button("Download Selected Videos"):
#         for link in selected_videos:
#             success = download_youtube_video(link, output_folder, "720p")
#             if not success:
#                 failed_downloads.append(link)

# # Provide a link to download the failed links as a text file
# if failed_downloads:
#     failed_links_file_path = os.path.join(output_folder, "failed_links.txt")
#     with open(failed_links_file_path, "w") as failed_file:
#         for link in failed_downloads:
#             failed_file.write(link + "\n")
select_videos()
