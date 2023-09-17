import streamlit as st

# Set the title of the Streamlit app
st.title("Text File Content Display")

# Add a file uploader for the user to upload a text file
text_file = st.file_uploader("Upload a text file:", type=["txt"])

# Check if a text file has been uploaded
if text_file:
    try:
        # Read and display the content of the text file
        file_content = text_file.read().decode("utf-8", "ignore")
        st.text(file_content)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# If no text file has been uploaded, display a message to the user
else:
    st.warning("Please upload a text file.")
