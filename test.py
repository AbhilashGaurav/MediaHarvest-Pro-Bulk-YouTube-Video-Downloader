import streamlit as st

st.title("Styled YouTube Video")

# Define custom CSS for the video
custom_css = """
<style>
.video-container {
    border-radius: 10px; /* Adjust the radius value as needed */
    overflow: hidden;
}
</style>
"""

# Display the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Embed a YouTube video using an iframe and apply the custom CSS
video_url = "https://www.youtube.com/watch?v=AtRf_eRQZwQ"  # Replace with your YouTube video ID
st.markdown(f'<div class="video-container"><iframe width="560" height="315" src="{video_url}" frameborder="0" allowfullscreen></iframe></div>', unsafe_allow_html=True)
