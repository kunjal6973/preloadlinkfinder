import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
def get_preloaded_links(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    preloaded_links = soup.find_all('link', rel='preload')
    urls = []
    for link in preloaded_links:
        href = link.get('href')
        urls.append(href)
    return urls
# Define the Streamlit app
def main():
    # Set the title of the app
    st.title('Extract Preloaded URLs from Webpages')
    
    # Create a file uploader for CSV files
    csv_file = st.file_uploader('Upload a CSV file', type=['csv'])
    
    # If a file is uploaded, read the contents and extract preloaded URLs
    if csv_file is not None:
        df = pd.read_csv(csv_file)
        urls = df['URLs']
        preloaded_links = []
        for url in urls:
            preloaded_links.append(get_preloaded_links(url))
        df['Preloaded Links'] = preloaded_links
        st.write(df)
        st.download_button(
            label='Download CSV',
            data=df.to_csv().encode('utf-8'),
            file_name='preloaded_links.csv',
            mime='text/csv'
        )

# Run the Streamlit app
if __name__ == '__main__':
    main()
streamlit run app.py
