# CTC Link Course Scraper

A comprehensive web scraper for extracting Summer 2025 course information from all Washington State Community Colleges using the CTC Link system.

## Features

- Scrapes Summer 2025 courses from all WA Community Colleges
- Two versions: basic (requests + BeautifulSoup) and enhanced (Selenium support)
- Handles JavaScript-heavy pages with Selenium
- Exports data to JSON and CSV formats
- Comprehensive logging and error handling
- Respectful rate limiting

## Files

- `ctclink_scraper.py` - Basic scraper using requests and BeautifulSoup
- `ctclink_scraper_enhanced.py` - Enhanced scraper with Selenium support
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Installation

1. Install Python 3.7+ if not already installed
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. For Selenium support, install ChromeDriver:
   - Download from https://chromedriver.chromium.org/
   - Add to PATH or place in project directory

## Usage

### Basic Scraper
```bash
python ctclink_scraper.py
```

### Enhanced Scraper (Recommended)
```bash
python ctclink_scraper_enhanced.py
```

The enhanced scraper will prompt you to:
- Choose whether to use Selenium (recommended: yes)
- Choose whether to run in headless mode (recommended: yes)

## Output Files

- `wa_cc_summer2025_courses.json` - Complete course data in JSON format
- `wa_cc_summer2025_courses.csv` - Course data in CSV format for spreadsheet analysis
- `wa_cc_summer2025_courses_enhanced.json` - Enhanced scraper JSON output
- `wa_cc_summer2025_courses_enhanced.csv` - Enhanced scraper CSV output

## Institution Codes

The scraper includes the following Washington State Community Colleges:

- WA230: Bellevue College
- WA240: Edmonds College
- WA245: Everett Community College
- WA250: Green River College
- WA255: Highline College
- WA260: Lake Washington Institute of Technology
- WA265: North Seattle College
- WA270: Olympic College
- WA275: Peninsula College
- WA280: Pierce College District
- WA285: Renton Technical College
- WA290: Seattle Central College
- WA300: Shoreline Community College
- WA305: Skagit Valley College
- WA310: South Puget Sound Community College
- WA315: South Seattle College
- WA320: Spokane Community College
- WA325: Spokane Falls Community College
- WA330: Tacoma Community College
- WA335: Walla Walla Community College
- WA340: Wenatchee Valley College
- WA345: Whatcom Community College
- WA350: Yakima Valley College

## Configuration

You can modify the institution codes in the `wa_cc_codes` dictionary within either scraper file to add, remove, or update institutions.

## Troubleshooting

### Common Issues

1. **No courses found**: 
   - Summer 2025 term may not be available yet
   - Website structure may have changed
   - Check network connectivity

2. **Selenium errors**:
   - Ensure ChromeDriver is installed and in PATH
   - Try running in non-headless mode for debugging
   - Check Chrome browser version compatibility

3. **Access denied**:
   - The website may have anti-bot protection
   - Try increasing delays between requests
   - Use different User-Agent strings

### Debugging

- Run the enhanced scraper in non-headless mode to see browser interactions
- Check log output for specific error messages
- Manually visit the URL to verify it's accessible

## Legal Considerations

- Ensure compliance with the website's terms of service
- Use reasonable delays between requests
- Consider contacting the institution for official data access
- This tool is for educational and research purposes

## Contributing

Feel free to submit issues or pull requests to improve the scraper's functionality or add support for additional institutions.

## Disclaimer

This scraper is provided as-is. The functionality may break if the CTC Link website structure changes. Always verify the accuracy of scraped data against official sources.