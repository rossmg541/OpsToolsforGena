# Web Content Fetcher

A simple Python script that downloads text content from multiple websites and saves it all into one organized text file.

## What Does This Do?

This script reads a list of website URLs from a file, visits each website, extracts all the text content, and saves everything into a single text document. It's perfect for:

- Creating offline copies of web articles
- Gathering research material from multiple sources
- Building a collection of content from various websites
- Archiving web content for later reading

## Before You Start

You'll need to have Python installed on your computer. Don't worry if you don't have it yet - here's how to check and install it:

### Check if Python is Installed

1. Open your terminal (Mac) or command prompt (Windows)
2. Type: `python --version` or `python3 --version`
3. If you see a version number (like "Python 3.9.0"), you're all set!

### Install Python (if needed)

- **Windows**: Download from [python.org](https://www.python.org/downloads/) and run the installer
- **Mac**: Python 3 usually comes pre-installed. If not, download from [python.org](https://www.python.org/downloads/)
- **Linux**: Usually pre-installed. If not, use your package manager: `sudo apt-get install python3`

## Installation

### Step 1: Download the Script

1. Download the `web_scraper.py` file to your computer
2. Put it in a folder where you'll remember it (like your Documents folder)

### Step 2: Install Required Libraries

This script needs two additional Python libraries. Open your terminal or command prompt and run these commands:

```bash
pip install requests beautifulsoup4
```

Or if that doesn't work, try:

```bash
pip3 install requests beautifulsoup4
```

## How to Use

### Step 1: Create Your URL List

Create a simple text file (like `urls.txt`) with one website URL per line:

```
https://example.com/article1
https://example.com/article2
wikipedia.org/some-page
```

**Note**: You can include or omit `https://` - the script will add it automatically if needed.

### Step 2: Run the Script

Open your terminal or command prompt, navigate to the folder with the script, and run:

```bash
python web_scraper.py "My Document Title" urls.txt
```

**Example**:
```bash
python web_scraper.py "Research on Climate Change" my_urls.txt
```

Or on some systems:
```bash
python3 web_scraper.py "Research on Climate Change" my_urls.txt
```

### Understanding the Command

- `python web_scraper.py` - Runs the script
- `"My Document Title"` - The title that will appear at the top of your output file (use quotes if it has spaces)
- `urls.txt` - The name of your file containing the URLs

### Step 3: Find Your Output

The script creates a new text file with all the content. The filename will be your title with underscores instead of spaces:

- Title: "Research on Climate Change" → File: `Research_on_Climate_Change.txt`

## Example Walkthrough

Let's say you want to save content from three cooking websites:

1. Create a file called `cooking_sites.txt`:
   ```
   https://www.seriouseats.com/best-pasta-recipe
   https://www.bonappetit.com/easy-desserts
   allrecipes.com/chicken-recipes
   ```

2. Run the command:
   ```bash
   python web_scraper.py "My Favorite Recipes" cooking_sites.txt
   ```

3. Open the new file `My_Favorite_Recipes.txt` to see all your content!

## Troubleshooting

### "Command not found" or "python is not recognized"

- Try using `python3` instead of `python`
- Make sure Python is installed and added to your PATH

### "No module named 'requests'" or "'bs4'"

- Run the installation command again: `pip install requests beautifulsoup4`
- Try `pip3` instead of `pip` if that doesn't work

### "Error fetching URL"

- Check that the URL is correct
- Make sure you have an internet connection
- Some websites may block automated access (this is normal)

### Script runs but creates an empty file

- The websites might be blocking automated access
- The URL might require login credentials (this script won't work for those)
- Try a different website to test

## Tips

- **Use quotes** around your document title if it contains spaces
- **One URL per line** in your URL file - no commas or extra formatting needed
- **Test with one URL first** to make sure everything works
- **Be patient** - if you have many URLs, it might take a minute or two to fetch everything
- **Respect websites** - don't overwhelm a single website with hundreds of requests

## What Gets Saved?

The output file includes:
- Your document title at the top
- For each URL:
  - The URL itself
  - All visible text from the webpage (no images or formatting)
  - A note if the content couldn't be retrieved

## Need Help?

If you run into issues:
1. Check that your URL file is formatted correctly (one URL per line)
2. Make sure the required libraries are installed
3. Try running the script with just one URL to isolate the problem
4. Check your internet connection

---

**License**: Free to use and modify for any purpose.
