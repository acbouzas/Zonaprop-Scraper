# Zonaprop-Scraper
Obtain argentinian real state data with this Zonaprop scraper.
Scrape property data from Zonaprop using this Python script. Extracted details include property URL, price, and location. The script uses Beautiful Soup for HTML parsing and Playwright for automated browsing.

## Usage

1. **Data Preparation:**
   - Create a CSV file named `hrefs.csv` with property URLs.

2. **Custom Configuration:**
   - Configure `headers` for Zonaprop requirements (ensure `'cookie': 'sessionId='` is correct).

3. **Dependencies:**
   - Install dependencies:
     ```bash
     pip install playwright playwright-sync bs4 pandas tqdm
     ```

4. **Running the Script:**
   - Modify `page_links` for specific Zonaprop pages.
   - The script processes links and extracts property data.

## Exception Handling

The script handles errors during scraping and logs failures for debugging.

## Important Notes

- Adjust script if Zonaprop's structure changes.
- Use a virtual environment for compatibility and to prevent package conflicts.

![script_example](https://github.com/acbouzas/Zonaprop-Scraper/blob/main/images/zonapropscreenshot.png)
![data_example]()
![exceptions_example]()
