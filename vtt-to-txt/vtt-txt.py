import re
import sys
import os

def vtt_to_txt(vtt_file_path, txt_file_path=None):
    """
    Convert a VTT (WebVTT) file to a plain text file.
    
    Args:
        vtt_file_path (str): Path to the input VTT file
        txt_file_path (str, optional): Path to the output TXT file. 
                                     If None, uses the same name with .txt extension
    """
    # Generate output filename if not provided
    if txt_file_path is None:
        base_name = os.path.splitext(vtt_file_path)[0]
        txt_file_path = base_name + '.txt'
    
    try:
        with open(vtt_file_path, 'r', encoding='utf-8') as vtt_file:
            content = vtt_file.read()
        
        # Split content into lines
        lines = content.split('\n')
        
        # Extract text lines (skip timestamps and metadata)
        text_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Skip the WEBVTT header
            if line.startswith('WEBVTT'):
                continue
                
            # Skip timestamp lines (format: 00:00:00.000 --> 00:00:00.000)
            if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}', line):
                continue
                
            # Skip cue settings (lines that might contain position, align, etc.)
            if '-->' in line:
                continue
                
            # Skip NOTE lines
            if line.startswith('NOTE'):
                continue
                
            # This should be subtitle text
            # Remove HTML-like tags if present (e.g., <i>, <b>, <u>)
            clean_line = re.sub(r'<[^>]+>', '', line)
            
            if clean_line:
                text_lines.append(clean_line)
        
        # Write to output file
        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write('\n'.join(text_lines))
        
        print(f"Successfully converted '{vtt_file_path}' to '{txt_file_path}'")
        print(f"Extracted {len(text_lines)} lines of text")
        
    except FileNotFoundError:
        print(f"Error: File '{vtt_file_path}' not found")
    except Exception as e:
        print(f"Error converting file: {e}")

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 2:
        print("Usage: python vtt_to_txt.py <input_vtt_file> [output_txt_file]")
        print("Example: python vtt_to_txt.py subtitles.vtt")
        print("Example: python vtt_to_txt.py subtitles.vtt output.txt")
        sys.exit(1)
    
    vtt_file = sys.argv[1]
    txt_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    vtt_to_txt(vtt_file, txt_file)

if __name__ == "__main__":
    main()