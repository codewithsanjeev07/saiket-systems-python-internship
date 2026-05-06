# SaiKet Systems Internship Tasks

This repository contains Python projects completed as part of the SaiKet Systems internship program. The tasks cover core Python programming, GUI development, file handling, API integration, web scraping, text processing, and structured data export.

The projects are built to be simple to run, easy to understand, and practical enough to demonstrate real-world programming concepts such as validation, exception handling, modular design, background processing, and user-friendly interfaces.

## Project Overview

The internship tasks are implemented as standalone Python applications. Most applications include a Tkinter-based graphical interface so users can interact with the program without using the command line.

The completed tasks include:

| Task | Project | Main File |
| --- | --- | --- |
| Task 1 | To-Do List Application | `task1_gui_replacement.py` |
| Task 2 | Number Guessing Game | `number_guessing_gui.py` |
| Task 3 | File Find and Replace Tool | `file_replace.py` |
| Task 4 | Expert-Level News Web Scraper | `web_scraper_gui.py` |
| Task 5 | Expert-Level Currency Converter | `currency_converter_gui.py` |
| Task 6 | Expert-Level Word Count Tool | `word_count_tool_gui.py` |

## Technologies Used

- Python 3
- Tkinter for desktop GUI development
- `urllib` for network requests
- `xml.etree.ElementTree` for RSS/XML parsing
- `json` and `csv` for structured exports
- `threading` for non-blocking GUI operations
- `pathlib` for modern file path handling
- Core Python modules for validation, file handling, and text analysis

No paid APIs or external API keys are required.

## Requirements

- Python 3.8 or later
- Internet connection for live news scraping and live currency rates
- Tkinter installed with Python

Tkinter is included with most standard Python installations. If it is missing, install a Python distribution that includes Tkinter.

## Installation

Clone or download the project folder, then open a terminal in the repository directory.

No third-party Python package installation is required for the main applications.

```bash
python --version
```

Use the command above to confirm that Python is installed.

## How to Run

Run any task from the terminal using:

```bash
python filename.py
```

Examples:

```bash
python web_scraper_gui.py
python currency_converter_gui.py
python word_count_tool_gui.py
```

On some systems, the command may be:

```bash
python3 filename.py
```

## Task 1: To-Do List Application

### Description

The To-Do List Application allows users to manage daily tasks through a simple interface. Users can add tasks, mark them as completed, view existing tasks, and manage their task list efficiently.

### Features

- Add new tasks
- View pending and completed tasks
- Mark tasks as completed
- Remove tasks
- GUI-based interaction
- Clean task organization

### Concepts Demonstrated

- Python data structures
- Conditional statements
- Event-driven programming
- Tkinter GUI design
- Basic state management

### File

- `task1_gui_replacement.py`

## Task 2: Number Guessing Game

### Description

The Number Guessing Game generates a random number and asks the user to guess it. The application provides hints after each guess and tracks the number of attempts.

### Features

- Random number generation
- User guess validation
- Higher/lower hints
- Attempt counter
- Guess history
- New game option
- GUI interface

### Concepts Demonstrated

- Random module usage
- Loops and conditions
- User input handling
- GUI event handling
- Game state management

### File

- `number_guessing_gui.py`

## Task 3: File Find and Replace Tool

### Description

The File Find and Replace Tool reads content from a text file, searches for a target word or phrase, replaces it with new content, and saves the updated file.

### Features

- Open and read text files
- Search for words or phrases
- Replace matching text
- Save modified output
- Handles missing files and invalid paths
- Includes sample text file for testing

### Concepts Demonstrated

- File input/output
- String manipulation
- Exception handling
- Text processing
- Working with external files

### Files

- `file_replace.py`
- `sample_text.txt`

## Task 4: Expert-Level News Web Scraper

### Description

The Expert-Level News Scraper collects headlines from multiple public RSS news feeds. It uses robust request handling, retry logic, rate limiting, XML parsing, structured output, and a Tkinter GUI for easy interaction.

Unlike a basic scraper that depends on fragile webpage HTML structure, this version uses RSS feeds where available. RSS is more stable, structured, and suitable for headline extraction.

### News Sources

The scraper supports the following RSS sources:

- BBC World
- NPR News
- New York Times
- The Guardian World

### Features

- Scrapes headlines from multiple sources
- Allows source selection using checkboxes
- Supports configurable headline limit per source
- Supports configurable delay between requests
- Includes retry logic for temporary network failures
- Includes request timeout control
- Uses a custom User-Agent header
- Parses RSS/XML safely
- Displays results in a table
- Shows status logs with timestamps
- Exports scraped results to JSON
- Exports scraped results to CSV
- Runs scraping in a background thread to keep the GUI responsive

### Error Handling

The scraper handles:

- HTTP errors
- Network errors
- Timeout errors
- Invalid RSS/XML responses
- Operating system errors
- Empty or invalid user input
- Missing source selection
- Export file write errors

### Output Fields

Each scraped headline contains:

- `source`
- `headline`
- `published`
- `url`
- `summary`
- `scraped_at`

### How to Run

```bash
python web_scraper_gui.py
```

### How to Use

1. Select one or more news sources.
2. Enter the number of headlines to fetch per source.
3. Set delay, retry count, and timeout values.
4. Click **Scrape Headlines**.
5. Review results in the table.
6. Export results using **Export JSON** or **Export CSV**.

### File

- `web_scraper_gui.py`

## Task 5: Expert-Level Currency Converter

### Description

The Expert-Level Currency Converter converts amounts between different currencies using live exchange rates. It fetches rates from a free public API and automatically falls back to offline snapshot rates if the API is unavailable.

### API Used

```text
https://open.er-api.com/v6/latest/USD
```

This endpoint provides exchange rates with USD as the base currency and does not require an API key for basic usage.

### Features

- Fetches live exchange rates
- Offline fallback rates when internet/API is unavailable
- Converts between supported currencies
- Supports many currency codes when live data is available
- Validates numeric amount input
- Prevents zero or negative conversions
- Allows currency swapping
- Refreshes rates on demand
- Maintains session conversion history
- Saves conversion history to a text file
- Uses a background thread while loading rates
- Keeps the GUI responsive during network requests

### Fallback Currencies

The fallback snapshot includes:

- USD
- INR
- EUR
- GBP
- JPY
- AUD
- CAD
- CHF
- CNY
- SGD

### Error Handling

The converter handles:

- HTTP errors
- Network errors
- Timeout errors
- Invalid API responses
- JSON parsing errors
- Unsupported currency selections
- Invalid amount input
- History file write errors

### History File

Conversions are saved to:

```text
currency_history.txt
```

Each entry includes:

- Timestamp
- Original amount
- Source currency
- Converted amount
- Target currency

### How to Run

```bash
python currency_converter_gui.py
```

### How to Use

1. Enter an amount.
2. Select the source currency.
3. Select the target currency.
4. Click **Convert**.
5. Use **Swap** to switch source and target currencies.
6. Use **Refresh Rates** to fetch the latest available rates.

### Files

- `currency_converter_gui.py`
- `currency_converter.py`

## Task 6: Expert-Level Word Count Tool

### Description

The Expert-Level Word Count Tool analyzes typed text or UTF-8 text files. It calculates basic text statistics, word frequency, and readability scores. It also supports JSON and CSV export.

The project is split into a reusable analysis module and a GUI application.

### Features

- Analyze pasted text
- Open and analyze UTF-8 files
- Count words
- Count lines
- Count total characters
- Count characters excluding spaces
- Count sentences
- Count paragraphs
- Generate word frequency results
- Optional stop-word filtering
- Configurable number of top words
- Calculate Flesch Reading Ease score
- Calculate Flesch-Kincaid Grade score
- Display a formatted report
- Copy report to clipboard
- Export analysis to JSON
- Export word frequency to CSV
- Keyboard shortcuts for common actions

### Readability Metrics

The tool includes:

- **Flesch Reading Ease:** Estimates how easy the text is to read.
- **Flesch-Kincaid Grade:** Estimates the approximate school grade level needed to understand the text.

### Keyboard Shortcuts

| Shortcut | Action |
| --- | --- |
| `Ctrl + O` | Open a file |
| `Ctrl + S` | Export JSON |
| `F5` | Analyze text |

### Error Handling

The word count tool handles:

- Invalid UTF-8 files
- Missing or unreadable files
- Invalid top-word limit
- Export errors
- Empty text input

### Export Options

The tool supports:

- JSON export for full analysis data
- CSV export for word frequency data

### How to Run

```bash
python word_count_tool_gui.py
```

### How to Use

1. Paste text into the input area or open a UTF-8 file.
2. Choose the number of top words to display.
3. Enable or disable stop-word filtering.
4. Click **Analyze** or press `F5`.
5. Review counts, readability scores, frequency table, and report.
6. Export the results or copy the report if needed.

### Files

- `word_count_tool.py`
- `word_count_tool_gui.py`

## Project Structure

```text
SaiKet-Systems-Internship/
├── README.md
├── task1_gui_replacement.py
├── number_guessing_gui.py
├── file_replace.py
├── sample_text.txt
├── web_scraper_gui.py
├── currency_converter.py
├── currency_converter_gui.py
├── word_count_tool.py
└── word_count_tool_gui.py
```

## Data Export Formats

### JSON

JSON export is used when full structured data is needed. It is useful for preserving nested data, timestamps, metadata, and complete analysis results.

### CSV

CSV export is used when results need to be opened in spreadsheet tools such as Microsoft Excel, Google Sheets, or LibreOffice Calc.

## Common Troubleshooting

### Python command not found

Install Python and ensure it is added to the system PATH. Then try:

```bash
python --version
```

or:

```bash
python3 --version
```

### Tkinter window does not open

Make sure your Python installation includes Tkinter. Standard Python installers for Windows usually include it by default.

### News scraper returns no results

Possible reasons:

- Internet connection is unavailable
- RSS feed is temporarily down
- The request timed out
- The selected source changed its RSS feed format

Try increasing the timeout or retry count.

### Currency converter uses fallback rates

This happens when live rates cannot be fetched. The app continues working using offline snapshot rates so the user can still perform conversions.

### Word count file does not open

The selected file must be valid UTF-8 text. Binary files or files saved with unsupported encodings may fail to load.

## Learning Outcomes

Through these projects, the following skills were practiced:

- Writing clean and modular Python code
- Building desktop GUI applications with Tkinter
- Handling user input and validation
- Working with files and directories
- Reading and writing JSON, CSV, and text files
- Fetching data from public web APIs
- Parsing RSS/XML data
- Managing network errors and timeouts
- Using retry logic and rate limiting
- Running background threads in GUI applications
- Processing text and calculating statistics
- Exporting structured program output

## Conclusion

This internship project helped strengthen practical Python development skills through a set of real-world applications. Each task demonstrates a different area of programming, from basic logic and file handling to GUI design, API usage, web scraping, and text analytics.

The final tasks, especially the news scraper, currency converter, and word count tool, include stronger validation, structured output, background processing, and error handling to make them more reliable and user friendly.
