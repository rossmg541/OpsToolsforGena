import os
import openai
import pandas as pd
import re
from tqdm import tqdm

# Ensure your OpenAI API key is set securely as an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set your OpenAI API key here securely

# Function to read transcripts from a CSV file and clean them
def read_and_clean_transcripts(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Check if the 'transcripts' column exists
    if 'transcripts' not in df.columns:
        raise KeyError("Column 'transcripts' not found in the DataFrame.")
    
    # Function to remove bracketed timestamps from a transcript
    def remove_timestamps(transcript):
        # Remove anything within square brackets including the brackets themselves
        cleaned_text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', transcript)
        return cleaned_text.strip()

    # Clean the 'transcripts' column
    df['cleaned_transcripts'] = df['transcripts'].apply(remove_timestamps)

    # Convert the cleaned transcripts to a list
    cleaned_transcripts = df['cleaned_transcripts'].tolist()
    return cleaned_transcripts

# Function to analyze a single transcript
def analyze_transcript(transcript):
    prompt = f"""
    You are an assistant helping to analyze customer feedback from meeting transcripts. Extract insights from the following transcript based on these criteria:

    1. **Satisfactions**: Points where customers express satisfaction with products or features.
    2. **Suggestions**: Subtle hints or direct suggestions about desired product enhancements or new features.
    3. **Complaints**: Any complaints or issues raised about current products or features.

    Provide the insights in a structured JSON format like:
    {{
      "satisfactions": ["Point 1", "Point 2", ...],
      "suggestions": ["Suggestion 1", "Suggestion 2", ...],
      "complaints": ["Complaint 1", "Complaint 2", ...]
    }}

    Here is the transcript:
    \"\"\"
    {transcript}
    \"\"\"
    """

    try:
        # Updated usage for openai.ChatCompletion.create() with the latest interface
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts insights from meeting transcripts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000,  # Increase max_tokens to allow more detailed responses
        )
        
        # Extract the response content
        insights = response.choices[0].message.content
        return insights.strip()
    except Exception as e:
        print(f"Error analyzing transcript: {e}")
        return None

# Function to process multiple transcripts
def process_transcripts(transcripts):
    insights_list = []
    for transcript in tqdm(transcripts, desc="Analyzing transcripts"):
        insights = analyze_transcript(transcript)
        if insights:
            insights_list.append(insights)
        else:
            insights_list.append('')  # Ensure the list remains the same length
    return insights_list

# Main function
def main():
    # Path to your CSV file containing transcripts
    csv_file = 'meeting_transcripts.csv'  # Replace with your CSV file path

    try:
        # Read and clean transcripts from the CSV file
        transcripts = read_and_clean_transcripts(csv_file)

        # Print a sample of cleaned transcripts for debugging
        print("Sample of cleaned transcripts:", transcripts[:2])  # Print first 2 cleaned transcripts
        
        # Process transcripts and extract insights
        insights_list = process_transcripts(transcripts)

        # Ensure both lists have the same length
        if len(transcripts) != len(insights_list):
            raise ValueError("The lengths of transcripts and insights do not match.")

        # Save the insights to a new CSV file
        output_df = pd.DataFrame({
            'transcript': transcripts,
            'insights': insights_list
        })
        output_df.to_csv('transcripts_insights.csv', index=False)
        print("Insights have been saved to 'transcripts_insights.csv'.")
    
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except pd.errors.EmptyDataError:
        print("File is empty. Please check the contents of the file.")
    except KeyError as e:
        print(f"KeyError: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
