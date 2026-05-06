"""SaiKet Systems — Internship
Task 4: Expert-Level Web Scraper
Scrapes news headlines from multiple sources with robust error handling,
rate limiting, retry logic, and structured output.
"""

import csv
import html
import json
import threading
import time
import tkinter as tk
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


NEWS_SOURCES = {
    "BBC World": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "NPR News": "https://feeds.npr.org/1001/rss.xml",
    "New York Times": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "The Guardian World": "https://www.theguardian.com/world/rss",
}

USER_AGENT = "Mozilla/5.0 (compatible; StudentNewsScraper/1.0)"


def clean_text(value):
    if value is None:
        return ""
    return html.unescape(value).strip()


def fetch_url(url, retries, timeout):
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(request, timeout=timeout) as response:
                return response.read()
        except HTTPError as error:
            last_error = f"HTTP {error.code}"
        except URLError as error:
            last_error = f"Network error: {error.reason}"
        except TimeoutError:
            last_error = "Request timed out"
        except OSError as error:
            last_error = f"System error: {error}"

        if attempt < retries:
            time.sleep(1.5 * attempt)

    raise RuntimeError(last_error or "Unknown network error")


def parse_rss_items(source_name, xml_bytes, limit):
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as error:
        raise ValueError(f"Invalid RSS/XML response: {error}")

    headlines = []

    for item in root.findall(".//item"):
        title = clean_text(item.findtext("title"))
        link = clean_text(item.findtext("link"))
        published = clean_text(item.findtext("pubDate"))
        description = clean_text(item.findtext("description"))

        if not title:
            continue

        headlines.append(
            {
                "source": source_name,
                "headline": title,
                "published": published,
                "url": link,
                "summary": description,
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

        if len(headlines) >= limit:
            break

    return headlines


def scrape_source(source_name, url, limit, retries, timeout):
    xml_bytes = fetch_url(url, retries=retries, timeout=timeout)
    return parse_rss_items(source_name, xml_bytes, limit)


class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expert-Level News Scraper")
        self.root.geometry("980x640")
        self.root.minsize(860, 540)

        self.results = []
        self.source_vars = {}
        self.limit_var = tk.StringVar(value="5")
        self.delay_var = tk.StringVar(value="1.0")
        self.retries_var = tk.StringVar(value="3")
        self.timeout_var = tk.StringVar(value="10")
        self.status_var = tk.StringVar(value="Ready.")

        self.build_ui()

    def build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main = ttk.Frame(self.root, padding=18)
        main.grid(row=0, column=0, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.rowconfigure(3, weight=1)

        header = ttk.Frame(main)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        ttk.Label(
            header,
            text="Expert-Level News Scraper",
            font=("Segoe UI", 18, "bold"),
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            header,
            text="Scrapes headlines from multiple public RSS sources with retries and rate limiting.",
        ).grid(row=1, column=0, sticky="w", pady=(4, 14))

        source_frame = ttk.LabelFrame(main, text="Sources", padding=10)
        source_frame.grid(row=1, column=0, sticky="ew")

        for column, source_name in enumerate(NEWS_SOURCES):
            selected = tk.BooleanVar(value=True)
            self.source_vars[source_name] = selected
            ttk.Checkbutton(
                source_frame,
                text=source_name,
                variable=selected,
            ).grid(row=0, column=column, sticky="w", padx=(0, 18))

        controls = ttk.Frame(main)
        controls.grid(row=2, column=0, sticky="ew", pady=14)

        self.add_labeled_entry(controls, "Headlines/source", self.limit_var, 0)
        self.add_labeled_entry(controls, "Delay seconds", self.delay_var, 2)
        self.add_labeled_entry(controls, "Retries", self.retries_var, 4)
        self.add_labeled_entry(controls, "Timeout", self.timeout_var, 6)

        self.scrape_button = ttk.Button(
            controls,
            text="Scrape Headlines",
            command=self.start_scraping,
        )
        self.scrape_button.grid(row=0, column=8, padx=(16, 0))

        ttk.Button(
            controls,
            text="Export JSON",
            command=self.export_json,
        ).grid(row=0, column=9, padx=(8, 0))

        ttk.Button(
            controls,
            text="Export CSV",
            command=self.export_csv,
        ).grid(row=0, column=10, padx=(8, 0))

        table_frame = ttk.Frame(main)
        table_frame.grid(row=3, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = ("source", "headline", "published", "url")
        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=14,
        )
        self.table.heading("source", text="Source")
        self.table.heading("headline", text="Headline")
        self.table.heading("published", text="Published")
        self.table.heading("url", text="URL")
        self.table.column("source", width=150, anchor="w")
        self.table.column("headline", width=430, anchor="w")
        self.table.column("published", width=210, anchor="w")
        self.table.column("url", width=300, anchor="w")
        self.table.grid(row=0, column=0, sticky="nsew")

        y_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview,
        )
        y_scroll.grid(row=0, column=1, sticky="ns")
        self.table.configure(yscrollcommand=y_scroll.set)

        log_frame = ttk.LabelFrame(main, text="Status Log", padding=8)
        log_frame.grid(row=4, column=0, sticky="ew", pady=(14, 0))
        log_frame.columnconfigure(0, weight=1)

        self.log_box = tk.Text(log_frame, height=5, wrap="word")
        self.log_box.grid(row=0, column=0, sticky="ew")
        self.log_box.configure(state="disabled")

        ttk.Label(main, textvariable=self.status_var).grid(
            row=5,
            column=0,
            sticky="w",
            pady=(10, 0),
        )

    def add_labeled_entry(self, parent, label, variable, column):
        ttk.Label(parent, text=label).grid(row=0, column=column, sticky="w")
        ttk.Entry(parent, textvariable=variable, width=8).grid(
            row=0,
            column=column + 1,
            padx=(6, 12),
        )

    def validate_settings(self):
        selected_sources = [
            name for name, selected in self.source_vars.items() if selected.get()
        ]
        if not selected_sources:
            messagebox.showerror("No Sources", "Please select at least one source.")
            return None

        try:
            limit = int(self.limit_var.get())
            retries = int(self.retries_var.get())
            timeout = float(self.timeout_var.get())
            delay = float(self.delay_var.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Settings",
                "Limit, delay, retries, and timeout must be valid numbers.",
            )
            return None

        if limit <= 0 or retries <= 0 or timeout <= 0 or delay < 0:
            messagebox.showerror(
                "Invalid Settings",
                "Use positive values. Delay can be zero or greater.",
            )
            return None

        return selected_sources, limit, retries, timeout, delay

    def start_scraping(self):
        settings = self.validate_settings()
        if settings is None:
            return

        self.results = []
        for row in self.table.get_children():
            self.table.delete(row)

        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", tk.END)
        self.log_box.configure(state="disabled")

        self.scrape_button.configure(state="disabled")
        self.status_var.set("Scraping in progress...")

        thread = threading.Thread(
            target=self.scrape_in_background,
            args=settings,
            daemon=True,
        )
        thread.start()

    def scrape_in_background(self, selected_sources, limit, retries, timeout, delay):
        total_found = 0

        for index, source_name in enumerate(selected_sources, start=1):
            url = NEWS_SOURCES[source_name]
            self.queue_log(f"Fetching {source_name}...")

            try:
                headlines = scrape_source(source_name, url, limit, retries, timeout)
                total_found += len(headlines)
                self.root.after(0, self.add_results, headlines)
                self.queue_log(f"Success: {source_name} returned {len(headlines)} headline(s).")
            except RuntimeError as error:
                self.queue_log(f"Failed: {source_name} - {error}")
            except ValueError as error:
                self.queue_log(f"Failed: {source_name} - {error}")

            if index < len(selected_sources) and delay > 0:
                self.queue_log(f"Rate limit: waiting {delay:.1f} second(s).")
                time.sleep(delay)

        self.root.after(0, self.finish_scraping, total_found)

    def queue_log(self, message):
        self.root.after(0, self.add_log, message)

    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_box.see(tk.END)
        self.log_box.configure(state="disabled")

    def add_results(self, headlines):
        self.results.extend(headlines)
        for item in headlines:
            self.table.insert(
                "",
                tk.END,
                values=(
                    item["source"],
                    item["headline"],
                    item["published"],
                    item["url"],
                ),
            )

    def finish_scraping(self, total_found):
        self.scrape_button.configure(state="normal")
        self.status_var.set(f"Done. Collected {total_found} headline(s).")

    def require_results(self):
        if self.results:
            return True
        messagebox.showwarning("No Results", "Scrape headlines before exporting.")
        return False

    def export_json(self):
        if not self.require_results():
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Save JSON export",
        )
        if not output_path:
            return

        try:
            Path(output_path).write_text(
                json.dumps(self.results, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            messagebox.showinfo("Export Complete", f"JSON saved to:\n{output_path}")
        except OSError as error:
            messagebox.showerror("Export Error", f"Could not save JSON.\n\n{error}")

    def export_csv(self):
        if not self.require_results():
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save CSV export",
        )
        if not output_path:
            return

        try:
            with Path(output_path).open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "source",
                        "headline",
                        "published",
                        "url",
                        "summary",
                        "scraped_at",
                    ],
                )
                writer.writeheader()
                writer.writerows(self.results)
            messagebox.showinfo("Export Complete", f"CSV saved to:\n{output_path}")
        except OSError as error:
            messagebox.showerror("Export Error", f"Could not save CSV.\n\n{error}")


def main():
    root = tk.Tk()
    WebScraperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
