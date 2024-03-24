import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_preloaded_links(url):
    try:
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        preloaded_links = soup.find_all('link', rel='preload')
        urls = [link.get('href') for link in preloaded_links]
        return urls
    except Exception as e:
        st.error(f"Error fetching preloaded links for {url}: {e}")
        return []

def main():
    st.title('Extract Preloaded URLs from Webpages')
    
    csv_file = st.file_uploader('Upload a CSV file', type=['csv'])
    
    if csv_file is not None:
        try:
            df = pd.read_csv(csv_file)
            urls = df['URLs'].dropna()  # Handle NaN values
            preloaded_links = [get_preloaded_links(url) for url in urls]
            df['Preloaded Links'] = preloaded_links
            st.write(df)
            st.download_button(
                label='Download CSV',
                data=df.to_csv(index=False).encode('utf-8'),  # Exclude index column
                file_name='preloaded_links.csv',
                mime='text/csv'
            )
        except Exception as e:
            st.error(f"Error processing CSV file: {e}")

if __name__ == '__main__':
    main()
