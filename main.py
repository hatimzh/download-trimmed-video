# from pytube import YouTube
import os
import subprocess

def download_and_trim_video(url, start_time, end_time, output_path):
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Define the video output filename for yt-dlp download (using .webm extension)
    output_file = os.path.join(output_path, 'downloaded_video.webm')
    
    # Download video using yt-dlp until end_time
    download_command = [
        'yt-dlp',
        url,
        '-o', output_file,
        '--download-sections', f'*0-{end_time}'  # Download from the start (0) to the given end_time
    ]
    
    print(f"Downloading video up to {end_time}...")
    subprocess.run(download_command, check=True)
    
    # Define the final output file after trimming
    trimmed_file = os.path.join(output_path, 'trimmed_video.mp4')
    
    # Trim the downloaded video using ffmpeg from start_time to end_time
    trim_command = [
        'ffmpeg',
        '-i', output_file,  # Use the correct .webm file
        '-ss', start_time,
        '-to', end_time,
        '-c:v', 'copy',
        '-c:a', 'copy',
        trimmed_file
    ]
    
    print(f"Trimming video from {start_time} to {end_time}...")
    subprocess.run(trim_command, check=True)
    
    print(f"Trimmed video saved to: {trimmed_file}")

# Example usage
download_and_trim_video('https://youtu.be/Z2hDVt7dNxM?si=V3D9S63MaXV10wsr', "00:00:25", "00:00:35", "output")
