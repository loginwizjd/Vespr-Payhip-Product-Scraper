# Vespr Payhip Scraper

![Vespr Payhip Scraper](https://img.shields.io/badge/Vespr-Payhip%20Scraper-brightgreen)

Vespr Payhip Scraper is a Python-based tool designed to scrape product data from Payhip stores. It allows users to extract product details such as titles, prices, descriptions, images, and links, and export the data in JSON or CSV formats. The scraper is user-friendly, supports custom Payhip URLs, and includes features like progress tracking and export options.

---

## Features

- **Custom URL Support**: Accepts any valid Payhip store URL and automatically appends `/collection/all` if missing.
- **Accurate Pagination**: Dynamically calculates the total number of pages to scrape.
- **Progress Tracking**: Displays real-time progress, including product titles, descriptions, and links.
- **Export Options**: Supports exporting data to:
  - JSON
  - CSV
- **Error Handling**: Handles invalid URLs, failed requests, and export issues gracefully.
- **Interactive Input**: Allows users to set delays between requests and choose export formats.
- **Professional Design**: Includes ANSI color-coded output and ASCII art for a polished look.

---

## Requirements

- Python 3.7 or higher
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`

Install the required libraries using:

```bash
pip install requests beautifulsoup4
```

---

## Usage

### 1. Clone the Repository
Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/vespr-payhip-scraper.git
cd vespr-payhip-scraper
```

### 2. Run the Scraper
Run the scraper script:

```bash
python scraper.py
```

### 3. Follow the Prompts
- Enter a valid Payhip URL (e.g., `https://payhip.com/ArtixTactical/collection/all`).
- Set a delay between requests (default is 1 second).
- Choose an export format (JSON or CSV).
- Provide a filename for the exported data.

---

## Example Output

### Console Output
```plaintext
 __      _______ _____   _____   _____   _____   _____   _____  
 \ \    / / ____|  __ \ |  __ \ |  __ \ |  __ \ / ____| |  __ \ 
  \ \  / / (___ | |__) || |__) || |__) || |__) | (___   | |__) |
   \ \/ / \___ \|  ___/ |  ___/ |  ___/ |  _  / \___ \  |  ___/ 
    \  /  ____) | |     | |     | |     | | \ \ ____) | | |     
     \/  |_____/|_|     |_|     |_|     |_|  \_\_____/  |_|     
                                                                
                  VS Vespr Payhip Scraper V1.1.0

Welcome to Vespr Payhip Scraper!
Scrape Payhip product pages and export data in JSON, CSV, or Google Drive.
----------------------------------------------------------
Enter Payhip URL: https://payhip.com/ArtixTactical
✅ URL corrected to: https://payhip.com/ArtixTactical/collection/all
Enter delay between requests (in seconds, default 1): 1
Total pages: 3
Scraping page: https://payhip.com/ArtixTactical/collection/all
[33.33%] Scraped: Product 1
    Description: This is a sample description...
    Link: https://payhip.com/product1
...
Export options:
1. Export to JSON
2. Export to CSV
Choose an export option (1/2): 1
Enter filename (without extension): products
✅ Data exported to products.json (JSON)
✅ Scraped 15 products.
```

---

## Features in Detail

### URL Validation
- Ensures the URL starts with `https://payhip.com/`.
- Automatically appends `/collection/all` if missing.
- Rejects invalid URLs and prompts the user to re-enter.

### Progress Tracking
- Displays the percentage of progress for each page and product.
- Shows product titles, descriptions (truncated), and links.

### Export Options
- **JSON**: Exports data in a structured JSON format.
- **CSV**: Exports data in a tabular CSV format.

---

## File Structure

```
vespr-payhip-scraper/
├── scraper.py       # Main scraper script
└── README.md        # Documentation
```

---

## Contributing

Contributions are welcome! If you have ideas for new features or improvements, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Disclaimer

This tool is intended for educational purposes only. Ensure you have permission to scrape data from any website before using this tool.

---

Let me know if you need further adjustments or additional features!