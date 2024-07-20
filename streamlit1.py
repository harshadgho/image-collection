import streamlit as st
import requests
import json


class UnsplashApp:
    #constructor to initialise accesskey and list for storing images
    def __init__(self):
        self.access_key = "XBjo24yGUIJW56QBlGiP500UgfdyuzMD9qIKd5Ecr-E"
        self.image_urls = []

    #function to get 6 images from the api
    def get_images_by_category(self, category, num_images=6):
        url = f"https://api.unsplash.com/photos/random?client_id={self.access_key}&query={category}&count={num_images}"
        response = requests.get(url)

        try:
            data = response.json()
        except json.JSONDecodeError:
            st.error("Error fetching data from the API. Please check your connection or try again later.")
            return []

        return [image_data["urls"]["regular"] for image_data in data]

    #func for downloading images
    def download_image(self, image_url):
        response = requests.get(image_url)
        return response.content

def main():
    st.set_page_config(layout="wide")
    st.title("Image Gallery")
    app = UnsplashApp()

    if "search" not in st.session_state:
        st.session_state.search = ""

    #creating a sidebar for searching predefined cateogories
    st.sidebar.title("Menu")
    selected_category = st.sidebar.selectbox("Select a Category", ["Nature", "Landscape", "Cityscape", "Animal Kingdom"], on_change=lambda: st.session_state.update({"search": ""}))

    #creating a search bar to search for custom images   
    custom_category = st.text_input("Search for a custom category:", key="search")

    #to check which category to use
    if custom_category:
        app.image_urls = app.get_images_by_category(custom_category.lower(), num_images=6)
    elif selected_category:
        app.image_urls = app.get_images_by_category(selected_category.lower(), num_images=6)

    #display images in two columns
    col1, col2 = st.columns(2)
    for i, image_url in enumerate(app.image_urls):
        with col1 if i % 2 == 0 else col2:
            st.image(image_url, caption=f"Image {i + 1}", use_column_width=True)
            image_data = app.download_image(image_url)
            st.download_button(f"Download {i + 1}", image_data, file_name=f"image_{i + 1}.jpg", mime="image/jpeg")
            open_in_new_tab_button = f"""
                <a href="{image_url}" target="_blank">
                    <button class="custom-button">Open Image {i + 1} in New Tab</button>
                </a>
            """
            st.markdown(open_in_new_tab_button, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
