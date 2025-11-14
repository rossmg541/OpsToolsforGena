#!/usr/bin/env python3
"""
WOFF to TTF Converter Script

This script converts WOFF (Web Open Font Format) files to TTF (TrueType Font) files.
Requires the fonttools library: pip install fonttools

Usage:
    python woff_to_ttf.py input.woff [output.ttf]
    python woff_to_ttf.py --batch folder_path
"""

import sys
import os
import argparse
from pathlib import Path

try:
    from fontTools.ttLib import TTFont
except ImportError:
    print("Error: fonttools library is required. Install it with: pip install fonttools")
    sys.exit(1)


def convert_woff_to_ttf(input_path, output_path=None):
    """
    Convert a single WOFF file to TTF format.
    
    Args:
        input_path (str): Path to the input WOFF file
        output_path (str, optional): Path for the output TTF file. 
                                   If None, uses input filename with .ttf extension
    
    Returns:
        bool: True if conversion successful, False otherwise
    """
    try:
        input_path = Path(input_path)
        
        # Validate input file
        if not input_path.exists():
            print(f"Error: Input file '{input_path}' does not exist.")
            return False
        
        if not input_path.suffix.lower() in ['.woff', '.woff2']:
            print(f"Warning: '{input_path}' doesn't appear to be a WOFF file.")
        
        # Determine output path
        if output_path is None:
            output_path = input_path.with_suffix('.ttf')
        else:
            output_path = Path(output_path)
        
        # Load the WOFF font
        print(f"Loading {input_path}...")
        font = TTFont(input_path)
        
        # Save as TTF
        print(f"Converting to {output_path}...")
        font.save(output_path)
        font.close()
        
        # Verify the output file was created
        if output_path.exists():
            file_size = output_path.stat().st_size
            print(f"✓ Successfully converted '{input_path.name}' to '{output_path.name}' ({file_size:,} bytes)")
            return True
        else:
            print(f"✗ Failed to create output file '{output_path}'")
            return False
            
    except Exception as e:
        print(f"✗ Error converting '{input_path}': {str(e)}")
        return False


def batch_convert(folder_path):
    """
    Convert all WOFF files in a folder to TTF format.
    
    Args:
        folder_path (str): Path to folder containing WOFF files
    
    Returns:
        tuple: (successful_conversions, total_files)
    """
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return 0, 0
    
    if not folder_path.is_dir():
        print(f"Error: '{folder_path}' is not a directory.")
        return 0, 0
    
    # Find all WOFF files
    woff_files = list(folder_path.glob("*.woff")) + list(folder_path.glob("*.woff2"))
    
    if not woff_files:
        print(f"No WOFF files found in '{folder_path}'")
        return 0, 0
    
    print(f"Found {len(woff_files)} WOFF file(s) in '{folder_path}'")
    print("-" * 50)
    
    successful = 0
    for woff_file in woff_files:
        if convert_woff_to_ttf(woff_file):
            successful += 1
        print()  # Add spacing between conversions
    
    return successful, len(woff_files)


def main():
    parser = argparse.ArgumentParser(
        description="Convert WOFF files to TTF format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s font.woff                    # Convert single file
  %(prog)s font.woff output.ttf         # Convert with custom output name
  %(prog)s --batch ./fonts              # Convert all WOFF files in folder
        """
    )
    
    parser.add_argument(
        'input',
        nargs='?',
        help='Input WOFF file or folder path (when using --batch)'
    )
    
    parser.add_argument(
        'output',
        nargs='?',
        help='Output TTF file path (optional for single file conversion)'
    )
    
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Convert all WOFF files in the specified folder'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='WOFF to TTF Converter 1.0'
    )
    
    args = parser.parse_args()
    
    # Show help if no arguments provided
    if not args.input:
        parser.print_help()
        return
    
    print("WOFF to TTF Converter")
    print("=" * 30)
    
    if args.batch:
        # Batch conversion mode
        successful, total = batch_convert(args.input)
        print("-" * 50)
        print(f"Batch conversion complete: {successful}/{total} files converted successfully")
        
        if successful < total:
            sys.exit(1)
    else:
        # Single file conversion mode
        success = convert_woff_to_ttf(args.input, args.output)
        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()