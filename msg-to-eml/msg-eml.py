#!/usr/bin/env python3
"""
MSG to EML Converter
Converts Microsoft Outlook .msg files to standard .eml format
"""

import os
import sys
import argparse
from email.message import EmailMessage
from email.utils import formatdate, parseaddr
from datetime import datetime
import extract_msg


def convert_msg_to_eml(msg_path, eml_path=None, debug=False):
    """
    Convert a .msg file to .eml format
    
    Args:
        msg_path (str): Path to the input .msg file
        eml_path (str): Path for the output .eml file (optional)
        debug (bool): Enable debug output
    
    Returns:
        str: Path to the created .eml file
    """
    
    # Generate output path if not provided
    if eml_path is None:
        base_name = os.path.splitext(msg_path)[0]
        eml_path = base_name + '.eml'
    
    try:
        # Open and parse the .msg file
        if debug:
            print(f"Opening MSG file: {msg_path}")
            
        with extract_msg.Message(msg_path) as msg:
            # Create a new email message
            email = EmailMessage()
            
            if debug:
                print(f"Subject: {getattr(msg, 'subject', 'None')}")
                print(f"Sender: {getattr(msg, 'sender', 'None')}")
                print(f"Has body: {hasattr(msg, 'body') and msg.body is not None}")
                print(f"Has HTML body: {hasattr(msg, 'htmlBody') and msg.htmlBody is not None}")
                print(f"Attachments count: {len(msg.attachments) if msg.attachments else 0}")
            
            # Set basic headers
            if msg.subject:
                email['Subject'] = str(msg.subject)
            
            if msg.sender:
                email['From'] = str(msg.sender)
            
            if msg.to:
                email['To'] = str(msg.to)
            
            if msg.cc:
                email['Cc'] = str(msg.cc)
            
            if msg.bcc:
                email['Bcc'] = str(msg.bcc)
            
            # Set date
            if msg.date:
                email['Date'] = msg.date.strftime('%a, %d %b %Y %H:%M:%S %z')
            else:
                email['Date'] = formatdate(localtime=True)
            
            # Set message ID if available
            if hasattr(msg, 'message_id') and msg.message_id:
                email['Message-ID'] = str(msg.message_id)
            
            # Set body content
            has_content = False
            
            # Handle text body
            if msg.body:
                try:
                    email.set_content(str(msg.body), charset='utf-8')
                    has_content = True
                except Exception as e:
                    print(f"Warning: Could not set text body: {e}")
            
            # Handle HTML body as alternative
            if msg.htmlBody:
                try:
                    if has_content:
                        # Add as alternative if we already have text content
                        email.add_alternative(str(msg.htmlBody), subtype='html', charset='utf-8')
                    else:
                        # Set as main content if no text body
                        email.set_content(str(msg.htmlBody), subtype='html', charset='utf-8')
                        has_content = True
                except Exception as e:
                    print(f"Warning: Could not set HTML body: {e}")
            
            # If no content was set, add a minimal message
            if not has_content:
                email.set_content("(No message content)", charset='utf-8')
            
            # Handle attachments
            if msg.attachments:
                if debug:
                    print(f"Processing {len(msg.attachments)} attachments...")
                    
                for i, attachment in enumerate(msg.attachments):
                    try:
                        if hasattr(attachment, 'data') and attachment.data:
                            # Get filename
                            filename = getattr(attachment, 'longFilename', None) or \
                                     getattr(attachment, 'shortFilename', f'attachment_{i}')
                            
                            if debug:
                                print(f"  Attachment {i}: {filename} ({len(attachment.data)} bytes)")
                            
                            # Determine MIME type from filename extension
                            import mimetypes
                            mime_type, _ = mimetypes.guess_type(filename)
                            if mime_type is None:
                                mime_type = 'application/octet-stream'
                            
                            if '/' in mime_type:
                                maintype, subtype = mime_type.split('/', 1)
                            else:
                                maintype, subtype = 'application', 'octet-stream'
                            
                            # Add attachment with proper MIME type
                            email.add_attachment(
                                attachment.data,
                                maintype=maintype,
                                subtype=subtype,
                                filename=filename
                            )
                        else:
                            if debug:
                                print(f"  Skipping attachment {i}: no data")
                                
                    except Exception as e:
                        filename = getattr(attachment, 'longFilename', f'attachment_{i}')
                        print(f"Warning: Could not process attachment '{filename}': {e}")
                        if debug:
                            import traceback
                            traceback.print_exc()
            
            # Write the .eml file
            with open(eml_path, 'w', encoding='utf-8') as f:
                f.write(str(email))
            
            print(f"Successfully converted {msg_path} to {eml_path}")
            return eml_path
            
    except Exception as e:
        print(f"Error converting {msg_path}: {e}")
        return None


def batch_convert(input_dir, output_dir=None, debug=False):
    """
    Convert all .msg files in a directory to .eml format
    
    Args:
        input_dir (str): Directory containing .msg files
        output_dir (str): Directory for output .eml files (optional)
    """
    
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    converted_count = 0
    failed_count = 0
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.msg'):
            msg_path = os.path.join(input_dir, filename)
            
            if output_dir:
                eml_filename = os.path.splitext(filename)[0] + '.eml'
                eml_path = os.path.join(output_dir, eml_filename)
            else:
                eml_path = None
            
            result = convert_msg_to_eml(msg_path, eml_path, debug)
            if result:
                converted_count += 1
            else:
                failed_count += 1
    
    print(f"\nBatch conversion complete:")
    print(f"  Converted: {converted_count} files")
    print(f"  Failed: {failed_count} files")


def main():
    parser = argparse.ArgumentParser(description="Convert .msg files to .eml format")
    parser.add_argument('input', help='Input .msg file or directory')
    parser.add_argument('-o', '--output', help='Output .eml file or directory')
    parser.add_argument('-d', '--debug', action='store_true', 
                       help='Enable debug output')
    parser.add_argument('-b', '--batch', action='store_true', 
                       help='Batch convert all .msg files in input directory')
    
    args = parser.parse_args()
    
    # Check if input exists
    if not os.path.exists(args.input):
        print(f"Error: Input path '{args.input}' does not exist")
        sys.exit(1)
    
    if args.batch or os.path.isdir(args.input):
        # Batch conversion
        if not os.path.isdir(args.input):
            print("Error: Input must be a directory for batch conversion")
            sys.exit(1)
        batch_convert(args.input, args.output, args.debug)
    else:
        # Single file conversion
        if not args.input.lower().endswith('.msg'):
            print("Error: Input file must have .msg extension")
            sys.exit(1)
        
        result = convert_msg_to_eml(args.input, args.output, args.debug)
        if not result:
            sys.exit(1)


if __name__ == "__main__":
    # Check if required library is installed
    try:
        import extract_msg
    except ImportError:
        print("Error: extract-msg library is required")
        print("Install it with: pip install extract-msg")
        sys.exit(1)
    
    main()