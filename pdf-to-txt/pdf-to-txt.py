import pypdf
import sys
import os
from pathlib import Path

def extract_text_from_pdf(pdf_path, output_path=None):
    """
    Extract text from a PDF file and save it to a text file.
    
    Args:
        pdf_path (str): Path to the input PDF file
        output_path (str, optional): Path for the output text file. 
                                   If None, creates a .txt file with the same name as the PDF
    
    Returns:
        str: The extracted text
    """
    
    # Validate input file exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    # Generate output path if not provided
    if output_path is None:
        pdf_name = Path(pdf_path).stem
        output_path = f"{pdf_name}.txt"
    
    try:
        # Open and read the PDF
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = pypdf.PdfReader(pdf_file)
            
            # Check if PDF is encrypted
            if pdf_reader.is_encrypted:
                print("Warning: PDF is encrypted. Attempting to decrypt...")
                # Try to decrypt with empty password
                success = pdf_reader.decrypt("")
                if not success:
                    raise Exception("Could not decrypt PDF. Password required.")
            
            # Extract text from all pages
            text_content = []
            total_pages = len(pdf_reader.pages)
            
            print(f"Processing {total_pages} pages...")
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                try:
                    text = page.extract_text()
                    text_content.append(f"--- Page {page_num} ---\n{text}\n")
                    print(f"Processed page {page_num}/{total_pages}")
                except Exception as e:
                    print(f"Warning: Could not extract text from page {page_num}: {e}")
                    text_content.append(f"--- Page {page_num} ---\n[Error extracting text]\n")
        
        # Combine all text
        full_text = "\n".join(text_content)
        
        # Save to text file
        with open(output_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(full_text)
        
        print(f"Text successfully extracted and saved to: {output_path}")
        print(f"Total characters extracted: {len(full_text)}")
        
        return full_text
        
    except Exception as e:
        print(f"Error processing PDF: {e}")
        raise

def main():
    """Main function to handle command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_text.py <pdf_file> [output_file]")
        print("Example: python pdf_to_text.py document.pdf")
        print("Example: python pdf_to_text.py document.pdf extracted_text.txt")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        extract_text_from_pdf(pdf_file, output_file)
    except Exception as e:
        print(f"Failed to extract text: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()