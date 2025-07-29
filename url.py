import os
import sys
import csv
import re
import requests
import subprocess
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError, PytubeError

def setup_directories():
    """Create necessary directories"""
    os.makedirs('downloads/full', exist_ok=True)
    os.makedirs('downloads/trimmed', exist_ok=True)
    os.makedirs('downloads/temp', exist_ok=True)

def extract_youtube_id(url):
    """Extract YouTube video ID from various URL formats"""
    # Handle standard YouTube URLs
    if 'youtube.com/watch' in url:
        query = urlparse(url).query
        params = parse_qs(query)
        return params.get('v', [None])[0]
    
    # Handle youtu.be short URLs
    if 'youtu.be' in url:
        return url.split('/')[-1].split('?')[0]
    
    return None

def sanitize_filename(name):
    """Create filesystem-safe filename"""
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'\s+', '_', name).strip()
    return name[:100]  # Limit filename length

def download_youtube_media(url, download_dir='downloads/full', custom_name=None):
    """Download YouTube video/audio using pytube with improved error handling"""
    try:
        # Extract clean YouTube URL
        video_id = extract_youtube_id(url)
        if not video_id:
            print("Invalid YouTube URL format")
            return None
            
        clean_url = f"https://www.youtube.com/watch?v={video_id}"
        
        yt = YouTube(
            clean_url,
            use_oauth=False,
            allow_oauth_cache=False
        )
        
        # Get best audio stream
        audio_stream = yt.streams \
            .filter(only_audio=True, file_extension='mp4') \
            .order_by('abr') \
            .desc() \
            .first()
            
        if not audio_stream:
            audio_stream = yt.streams \
                .filter(only_audio=True) \
                .order_by('abr') \
                .desc() \
                .first()
            
        if not audio_stream:
            print("No suitable audio stream found")
            return None
            
        # Determine filename
        if custom_name:
            base_name = sanitize_filename(custom_name)
        else:
            base_name = sanitize_filename(yt.title)
            
        # Use appropriate extension
        ext = 'm4a' if 'mp4' in audio_stream.mime_type else 'webm'
        filename = f"{base_name}.{ext}"
        filepath = os.path.join(download_dir, filename)
        
        # Download to temp location first
        temp_filename = f"temp_{video_id}.{ext}"
        temp_path = os.path.join('downloads/temp', temp_filename)
        
        print(f"Downloading YouTube audio: {yt.title}")
        audio_stream.download(
            output_path='downloads/temp',
            filename=temp_filename
        )
        
        # Move to final location
        os.rename(temp_path, filepath)
        print(f"Downloaded: {filename}")
        return filepath
        
    except (VideoUnavailable, RegexMatchError, KeyError, PytubeError) as e:
        print(f"YouTube download error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        
    return None

# Rest of the code remains the same as before (extract_download_links, download_generic_media, etc.)
# Only changing the process_urls function to handle custom names better

def process_urls(csv_path):
    """Process all URLs from the CSV file with improved error handling"""
    with open(csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row_idx, row in enumerate(reader):
            if not row or not row[0].strip():
                continue
                
            url = row[0].strip()
            trim_csv = row[1].strip() if len(row) > 1 and row[1].strip() else None
            custom_name = row[2].strip() if len(row) > 2 and row[2].strip() else None
            
            print(f"\n{'='*50}")
            print(f"Processing URL #{row_idx+1}")
            print(f"URL: {url}")
            if custom_name:
                print(f"Custom name: {custom_name}")
            if trim_csv:
                print(f"Trim CSV: {trim_csv}")
            
            # Handle YouTube URLs
            if any(domain in url for domain in ['youtube.com', 'youtu.be']):
                downloaded_file = download_youtube_media(url, custom_name=custom_name)
                if downloaded_file and trim_csv:
                    process_trim_csv(trim_csv, downloaded_file)
                continue
            
            # Resolve short URLs
            final_url = resolve_url(url)
            if not final_url:
                print("Skipping - could not resolve URL")
                continue
                
            # Handle YouTube after redirection
            if any(domain in final_url for domain in ['youtube.com', 'youtu.be']):
                downloaded_file = download_youtube_media(final_url, custom_name=custom_name)
                if downloaded_file and trim_csv:
                    process_trim_csv(trim_csv, downloaded_file)
                continue
                
            # Handle generic services
            download_links = extract_download_links(final_url)
            if not download_links:
                print("No media links found")
                continue
                
            # Download first valid media file
            downloaded_file = None
            for media_url in download_links:
                downloaded_file = download_generic_media(media_url, custom_name=custom_name)
                if downloaded_file:
                    break
            
            # Process trimming
            if downloaded_file and trim_csv:
                process_trim_csv(trim_csv, downloaded_file)

# Main function remains the same