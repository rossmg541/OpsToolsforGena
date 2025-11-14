#!/usr/bin/env python3
import os
import sys
import subprocess

# Define the base path and directory structure
BASE_PATH = "/Users/typeface/Documents/Operational-Tools-Automation/gif-maker"
INPUT_DIR = os.path.join(BASE_PATH, "video-files")
OUTPUT_DIR = os.path.join(BASE_PATH, "gifs")

def convert_to_gif(input_file, output_file=None, fps=10, scale=1800):
    """
    Convert a video file (.mp4 or .webm) to an animated GIF using FFmpeg.
    """
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return False
    
    # Check file extension
    _, ext = os.path.splitext(input_file)
    if ext.lower() not in ['.mp4', '.webm']:
        print(f"Error: Unsupported file format '{ext}'. Only .mp4 and .webm are supported.")
        return False
    
    # Create output filename if not provided
    if output_file is None:
        filename = os.path.basename(input_file)
        base_filename = os.path.splitext(filename)[0]
        output_file = os.path.join(OUTPUT_DIR, base_filename + '.gif')
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    try:
        # Build FFmpeg command
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-vf', f'fps={fps},scale={scale}:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse',
            '-loop', '0',
            output_file
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        
        # Execute FFmpeg
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error during conversion: {result.stderr}")
            return False
        else:
            print(f"Conversion complete! GIF saved to: {output_file}")
            return True
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

def process_directory():
    """Process all supported video files in the input directory"""
    # Check if input directory exists
    if not os.path.exists(INPUT_DIR):
        print(f"Error: Input directory '{INPUT_DIR}' not found.")
        return False
    
    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")
    
    # Get all video files
    video_files = []
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(('.mp4', '.webm')):
            video_files.append(os.path.join(INPUT_DIR, filename))
    
    if not video_files:
        print(f"No .mp4 or .webm files found in {INPUT_DIR}")
        return False
    
    # Process each video file
    print(f"Found {len(video_files)} video files to process.")
    for video_file in video_files:
        convert_to_gif(video_file)
    
    return True

def process_single_file(filename, fps=10, scale=1800):
    """Process a single file from the input directory"""
    input_file = os.path.join(INPUT_DIR, filename)
    output_file = os.path.join(OUTPUT_DIR, os.path.splitext(filename)[0] + '.gif')
    return convert_to_gif(input_file, output_file, fps, scale)

def main():
    # Check command line arguments
    if len(sys.argv) == 1:
        # No arguments, process all files in the directory
        process_directory()
    elif len(sys.argv) >= 2:
        if sys.argv[1] == "--all":
            # Process all files
            process_directory()
        else:
            # Process a specific file
            filename = sys.argv[1]
            
            fps = 10
            if len(sys.argv) >= 3:
                try:
                    fps = int(sys.argv[2])
                except ValueError:
                    print("Warning: Invalid fps value. Using default (10).")
            
            scale = 1800
            if len(sys.argv) >= 4:
                try:
                    scale = int(sys.argv[3])
                except ValueError:
                    print("Warning: Invalid scale value. Using default (320).")
            
            process_single_file(filename, fps, scale)

if __name__ == "__main__":
    main()