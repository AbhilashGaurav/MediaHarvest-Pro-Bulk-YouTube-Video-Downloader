from pytube import YouTube
import streamlit as st
import os

# Set the title of the Streamlit app
st.title("YouTube Video Download")

# Add a text input field for the user to enter the YouTube video link
video_url = st.text_input("Enter YouTube Video URL:")

# Create a flag to indicate if the video has been downloaded
video_downloaded = False

# Check if a video URL has been provided by the user
if video_url:
    try:
        # Create a YouTube object using the provided URL
        yt = YouTube(video_url)

        # Get the title of the video
        video_title = yt.title

        # Display the video title
        st.write(f"Video Title: {video_title}")

        # Get the streams available for the video
        video_streams = yt.streams

        # Create a selectbox for the user to choose the video quality
        selected_stream = st.selectbox("Select Video Quality:", [stream.resolution for stream in video_streams])

        # Find the stream with the selected quality
        selected_stream = next(stream for stream in video_streams if stream.resolution == selected_stream)

        # Specify the output path to save the video
        output_path = "video"

        # Add a button to download the video
        if st.button("Download Video"):
            # Download the video
            selected_stream.download(output_path)
            video_downloaded = True
            st.success(f"Video downloaded successfully.")

        # Provide a link to download the downloaded video if it has been downloaded
        if video_downloaded:
            video_file_path = os.path.join(output_path, f"{yt.title}.mp4")
            with open(video_file_path, "rb") as video_file:
                video_bytes = video_file.read()
            st.download_button(label="Click to Download", data=video_bytes, key=f"download_button_{yt.title}", file_name=f"{yt.title}.mp4")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# If no video URL has been provided, display a message to the user
else:
    st.warning("Please enter a valid YouTube video URL.")
