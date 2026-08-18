# Web Scraping Practice Project

This project is a Python web scraper that extracts book information from [Books to Scrape](http://books.toscrape.com/) and saves it into an Excel file.

## What the script does

The script:

- requests the main page of the bookstore
- finds all book categories from the sidebar
- visits each category page
- collects links to every book in that category
- scrapes each book's details
- exports the results to an Excel workbook named `scraped_books.xlsx`

## Extracted data

For each book, the scraper captures:

- Book title
- UPC
- Image URL
- Price excluding tax
- Price including tax
- Tax
- In-stock status
- Number of reviews
- Rating
- Description

## Project files

- `scrapingBooks.py` — main scraping script
- `scraped_books.xlsx` — generated Excel output file
- `README.md` — project documentation

## Requirements

Install the required Python packages:

```bash
pip install requests beautifulsoup4 lxml openpyxl
```

## Run the script

From the project folder, run:

```bash
python scrapingBooks.py
```

On Windows, you may also use:

```bash
py scrapingBooks.py
```

## Output

When the script finishes successfully, it creates:

```text
scraped_books.xlsx
```

This file is saved in the same folder as the script.

## Notes

- The scraper uses the public demo website `books.toscrape.com` for practice.
- The site is meant for educational scraping and testing.
- Please avoid overloading servers and respect the website's usage policies.

## Example workflow

1. Install dependencies
2. Run the script
3. Open the generated Excel file
4. Review the scraped book data by category
