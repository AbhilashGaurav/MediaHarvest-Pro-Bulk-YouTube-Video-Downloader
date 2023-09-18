import streamlit as st
from pytube import YouTube
import os
import zipfile
import shutil


# Function to download YouTube video under a specified duration limit
def download_youtube_video(link, output_path, quality, duration_limit):
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
st.title("Bulk YouTube Video Downloader")

# Initialize selected_video_links as an empty list
selected_video_links = []

# Add a file uploader for the user to upload a text file containing YouTube links
video_links_file = st.file_uploader("Upload a text file with YouTube video links:", type=["txt"])

# Create an output folder to save the videos
output_folder = "downloaded_videos"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Create a list to store failed downloads
failed_downloads = []

# Checkbox to enable/disable duration limit
if video_links_file is not None:
    enable_duration_limit = st.sidebar.checkbox("Enable Duration Limit")

# Set default duration limit value
duration_limit = None

# If duration limit is enabled, display the slider
if video_links_file and enable_duration_limit:
    duration_limit = st.sidebar.slider("Set Duration Limit (seconds):", min_value=1, max_value=600, value=120)

# Check if a video links file has been uploaded
if video_links_file:
    try:
        # Read YouTube links from the uploaded text file
        youtube_links = video_links_file.read().decode("utf-8", "ignore").splitlines()

        # Create a list to store selected video links
        selected_video_links = []

        # Add a "Select All" button
        select_all = st.checkbox("Select All")

        # Create a selectbox for the user to choose video quality
        video_quality = st.sidebar.selectbox("Select Video Quality:", ["144p", "360p", "720p", "1080p"])

        # Iterate through the list of video links and display a checkbox for each
        for link in youtube_links:
            st.write(link)
            if select_all:
                selected = True
            else:
                selected = st.checkbox(f"Select '{link}' for download")
            if selected:
                selected_video_links.append(link)

        # Provide a button to download the selected videos
        if selected_video_links:
            if st.button("Download Selected Videos"):
                for link in selected_video_links:
                    success = download_youtube_video(link, output_folder, video_quality, duration_limit)
                    if not success:
                        failed_downloads.append(link)

        # Provide a link to download the failed links as a text file
        if failed_downloads:
            failed_links_file_path = os.path.join(output_folder, "failed_links.txt")
            with open(failed_links_file_path, "w") as failed_file:
                for link in failed_downloads:
                    failed_file.write(link + "\n")

    except Exception as e:
        pass

# Check if the output_folder contains downloaded videos before showing the "Download All Videos as ZIP" button
if os.listdir(output_folder) and video_links_file:
    if st.button("Download All Videos as ZIP"):
        # Create a ZIP file containing all videos
        zip_filename = "downloaded_videos.zip"
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(output_folder):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), output_folder))

        # Provide a download link for the ZIP file
        with open(zip_filename, "rb") as zip_file:
            zip_data = zip_file.read()
        st.download_button(label="Confirm Download", data=zip_data, file_name=zip_filename)

        # Delete all files in the output_folder to empty it
        for file in os.listdir(output_folder):
            file_path = os.path.join(output_folder, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                st.error(f"An error occurred while deleting files: {str(e)}")

# If no video links file has been uploaded, display a message to the user
elif video_links_file is None:
    for file in os.listdir(output_folder):
        file_path = os.path.join(output_folder, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"An error occurred while deleting files: {str(e)}")
    st.warning("Please upload a text file containing YouTube video links.")


