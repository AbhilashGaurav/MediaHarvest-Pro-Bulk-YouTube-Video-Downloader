# import streamlit as st
# from googleapiclient.discovery import build
# from pytube import YouTube
# import os
# import zipfile
# import shutil
# # Set the title of the Streamlit app
# st.title("YouTube Video Search")

# # User input: Search query
# search_query = st.text_input("Enter your YouTube search query:")

# # YouTube Data API key (replace with your API key)
# api_key = "AIzaSyBZbpgzQJKPiXAxUCzkRre8sI3zYDaoAow"
# all_fetched_link=[]
# if st.button("Search"):
#     try:
#         if search_query:
#             # Create a YouTube Data API client
#             youtube = build("youtube", "v3", developerKey=api_key)
    
#             # Perform the YouTube video search with 'part' parameter
#             search_response = youtube.search().list(
#                 q=search_query,
#                 type="video",
#                 maxResults=10,  # Adjust the number of results as needed
#                 part="snippet"  # Include 'snippet' data in the response
#             ).execute()
    
#             # Display search results
    
#             for search_result in search_response.get("items", []):
#                 video_title = search_result["snippet"]["title"]
#                 video_url = f'https://www.youtube.com/watch?v={search_result["id"]["videoId"]}'
#                 # st.write(f"**Title:** {video_title}")
#                 # st.write(f"**URL:** [{video_url}]({video_url})")
#                 # st.write(f"**URL:** [{video_url}]({video_url})")
#                 # st.checkbox(f"{video_url} for download")
#                 # st.image(search_result["snippet"]["thumbnails"]["default"]["url"])
#                 temp_data=[]
#                 temp_data.append(video_title)
#                 temp_data.append(video_url)
#                 temp_data.append(search_result["snippet"]["thumbnails"]["default"]["url"])
#                 all_fetched_link.append(temp_data)
    
#         else:
#             st.warning("Please enter a search query.")
#     except Exception as e:
#         pass

# final_select=[]
# if all_fetched_link:
#     select_all = st.checkbox("Select All")

#     count=0
#     for ele in all_fetched_link:
#         st.write(f"**Title:** {ele[0]}")
#         # selected=st.checkbox(f"{ele[1]} for download")
#         # st.write(f"**URL:** {ele[1]}")
#         st.image(ele[2])
#         if select_all:
#             selected = True
#         else:
#             selected = st.checkbox(f"Select{ele[1]}")
#             print(selected," line 62")
#         if selected:
#             final_select.append(count)
#             print(final_select)
#         count+=1


#     # print(all_fetched_link)

# # Create a card-like layout using HTML and CSS
# card_html = """
#     <div style="
#         padding: 10px;
#         border: 1px solid #ccc;
#         border-radius: 5px;
#         box-shadow: 2px 2px 5px 0px rgba(0,0,0,0.3);
#         background-color: #f9f9f9;
#     ">
#         <h2>Card Title</h2>
#         <p>This is the content of the card.</p>
#         <img src="https://via.placeholder.com/150" alt="Card Image">
#         <button>Click me</button>
#     </div>
# """

# # Render the card using st.markdown
# st.markdown(card_html, unsafe_allow_html=True)

import streamlit as st
from googleapiclient.discovery import build
from pytube import YouTube
import os
import zipfile
import shutil
import json

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
api_key = "AIzaSyBZbpgzQJKPiXAxUCzkRre8sI3zYDaoAow"

# Initialize a list to store video data
all_fetched_links = []

# Initialize a list to store selected video URLs
selected_videos = []

search_response = {}

if st.button("Search"):
    try:
        if search_query:
            # Create a YouTube Data API client
            youtube = build("youtube", "v3", developerKey=api_key)

            # Perform the YouTube video search with 'part' parameter
            search_response = youtube.search().list(
                q=search_query,
                type="video",
                maxResults=10,  # Adjust the number of results as needed
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

def display_results(search_response):
    if search_response:
        for search_result in search_response.get("items", []):
            video_title = search_result["snippet"]["title"]
            video_url = f'https://www.youtube.com/watch?v={search_result["id"]["videoId"]}'
            thumbnail_url = search_result["snippet"]["thumbnails"]["default"]["url"]
            all_fetched_links.append({"title": video_title, "url": video_url, "thumbnail": thumbnail_url})
            # selected = st.checkbox(f"Select '{video_title}'", value=video_url in selected_videos)
            # if selected:
            #     selected_videos.append(video_url)
            st.write(f"**Title:** {video_title}")
            st.image(thumbnail_url)
            # call(all_fetched_links)
# Display selected videos
# display_results(search_response)

file_name = "json_search_response.json"  # Replace with your file name

# Open the JSON file for reading
with open(file_name, 'r') as json_file:
    # Parse the JSON data into a Python dictionary
    data = json.load(json_file)
for item in data.get('items', []):
    video_url=f'https://www.youtube.com/watch?v={item["id"]["videoId"]}'
    video_title = item["snippet"]["title"]
    selected = st.checkbox(f"Select '{video_title}'", value=video_url)
    if selected:
        selected_videos.append(video_url)

if selected_videos:
    st.subheader("Selected Videos:")
    for selected_video_url in selected_videos:
        st.write(selected_video_url)

# Provide a button to download the selected videos
if selected_videos:
    if st.button("Download Selected Videos"):
        for link in selected_videos:
            success = download_youtube_video(link, output_folder, "720p")
            if not success:
                failed_downloads.append(link)

# Provide a link to download the failed links as a text file
if failed_downloads:
    failed_links_file_path = os.path.join(output_folder, "failed_links.txt")
    with open(failed_links_file_path, "w") as failed_file:
        for link in failed_downloads:
            failed_file.write(link + "\n")
