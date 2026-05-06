"""SaiKet Systems — Internship
Task 5: Expert-Level Currency Converter
- Fetches live rates from exchangerate-api.com (free tier, no key needed)
- Falls back to a hardcoded snapshot when offline
- Full input validation, error handling, history log, and CLI menu
"""

import json
import threading
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


API_URL = "https://open.er-api.com/v6/latest/USD"
HISTORY_FILE = Path("currency_history.txt")

FALLBACK_RATES = {
    "USD": 1.0,
    "INR": 83.35,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 151.50,
    "AUD": 1.52,
    "CAD": 1.36,
    "CHF": 0.90,
    "CNY": 7.24,
    "SGD": 1.35,
}


def fetch_live_rates():
    try:
        with urlopen(API_URL, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        if data.get("result") != "success":
            error_type = data.get("error-type", "unknown error")
            raise ValueError(f"API returned an error: {error_type}")

        rates = data.get("rates")
        if not isinstance(rates, dict) or not rates:
            raise ValueError("API response did not include exchange rates.")

        return rates, "live", ""
    except HTTPError as error:
        error_message = f"HTTP error: {error.code}"
    except URLError as error:
        error_message = f"Network error: {error.reason}"
    except TimeoutError:
        error_message = "Request timed out."
    except (json.JSONDecodeError, ValueError) as error:
        error_message = f"Invalid API response: {error}"
    except OSError as error:
        error_message = f"System error: {error}"

    return FALLBACK_RATES.copy(), "offline fallback", error_message


def save_history_entry(entry):
    try:
        with HISTORY_FILE.open("a", encoding="utf-8") as file:
            file.write(entry + "\n")
    except OSError as error:
        messagebox.showwarning(
            "History Warning",
            f"Could not write history log.\n\nDetails: {error}",
        )


def convert_currency(amount, from_currency, to_currency, rates):
    amount_in_usd = amount / rates[from_currency]
    return amount_in_usd * rates[to_currency]


class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expert Currency Converter")
        self.root.geometry("720x520")
        self.root.minsize(620, 460)

        self.rates = FALLBACK_RATES.copy()
        self.rate_source = "offline fallback"
        self.history = []

        self.amount_var = tk.StringVar()
        self.from_var = tk.StringVar(value="USD")
        self.to_var = tk.StringVar(value="INR")
        self.result_var = tk.StringVar(value="Enter an amount and choose currencies.")
        self.status_var = tk.StringVar(value="Loading rates...")

        self.build_ui()
        self.refresh_rates()

    def build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main = ttk.Frame(self.root, padding=20)
        main.grid(row=0, column=0, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.rowconfigure(4, weight=1)

        title = ttk.Label(
            main,
            text="Expert-Level Currency Converter",
            font=("Segoe UI", 18, "bold"),
        )
        title.grid(row=0, column=0, sticky="w")

        attribution = ttk.Label(
            main,
            text="Rates by Exchange Rate API - https://www.exchangerate-api.com",
            font=("Segoe UI", 9),
        )
        attribution.grid(row=1, column=0, sticky="w", pady=(4, 18))

        form = ttk.Frame(main)
        form.grid(row=2, column=0, sticky="ew")
        form.columnconfigure((0, 1, 2), weight=1)

        ttk.Label(form, text="Amount").grid(row=0, column=0, sticky="w")
        ttk.Label(form, text="From").grid(row=0, column=1, sticky="w", padx=(12, 0))
        ttk.Label(form, text="To").grid(row=0, column=2, sticky="w", padx=(12, 0))

        amount_entry = ttk.Entry(form, textvariable=self.amount_var)
        amount_entry.grid(row=1, column=0, sticky="ew", pady=(6, 0))
        amount_entry.focus()

        self.from_combo = ttk.Combobox(
            form,
            textvariable=self.from_var,
            state="readonly",
            values=sorted(self.rates),
        )
        self.from_combo.grid(row=1, column=1, sticky="ew", padx=(12, 0), pady=(6, 0))

        self.to_combo = ttk.Combobox(
            form,
            textvariable=self.to_var,
            state="readonly",
            values=sorted(self.rates),
        )
        self.to_combo.grid(row=1, column=2, sticky="ew", padx=(12, 0), pady=(6, 0))

        actions = ttk.Frame(main)
        actions.grid(row=3, column=0, sticky="ew", pady=18)
        actions.columnconfigure(3, weight=1)

        ttk.Button(actions, text="Convert", command=self.convert).grid(row=0, column=0)
        ttk.Button(actions, text="Swap", command=self.swap_currencies).grid(
            row=0,
            column=1,
            padx=(10, 0),
        )
        ttk.Button(actions, text="Refresh Rates", command=self.refresh_rates).grid(
            row=0,
            column=2,
            padx=(10, 0),
        )

        result = ttk.Label(
            main,
            textvariable=self.result_var,
            font=("Segoe UI", 14, "bold"),
            wraplength=660,
        )
        result.grid(row=4, column=0, sticky="nw", pady=(0, 14))

        history_frame = ttk.LabelFrame(main, text="Session History", padding=10)
        history_frame.grid(row=5, column=0, sticky="nsew")
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)

        self.history_box = tk.Listbox(history_frame, height=8)
        self.history_box.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self.history_box.yview,
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.history_box.configure(yscrollcommand=scrollbar.set)

        status = ttk.Label(main, textvariable=self.status_var)
        status.grid(row=6, column=0, sticky="w", pady=(12, 0))

        self.root.bind("<Return>", lambda _event: self.convert())

    def refresh_rates(self):
        self.status_var.set("Loading live rates...")
        self.set_controls_enabled(False)

        thread = threading.Thread(target=self.load_rates_in_background, daemon=True)
        thread.start()

    def load_rates_in_background(self):
        rates, source, error_message = fetch_live_rates()
        self.root.after(0, self.apply_loaded_rates, rates, source, error_message)

    def apply_loaded_rates(self, rates, source, error_message):
        old_from = self.from_var.get()
        old_to = self.to_var.get()

        self.rates = rates
        self.rate_source = source
        codes = sorted(self.rates)
        self.from_combo.configure(values=codes)
        self.to_combo.configure(values=codes)

        self.from_var.set(old_from if old_from in self.rates else "USD")
        self.to_var.set(old_to if old_to in self.rates else "INR")

        if error_message:
            self.status_var.set(f"Using offline fallback rates. {error_message}")
        else:
            self.status_var.set("Live rates loaded successfully.")

        self.set_controls_enabled(True)

    def set_controls_enabled(self, enabled):
        state = "normal" if enabled else "disabled"
        combo_state = "readonly" if enabled else "disabled"

        for child in self.root.winfo_children():
            self.set_child_state(child, state, combo_state)

    def set_child_state(self, widget, state, combo_state):
        for child in widget.winfo_children():
            if isinstance(child, ttk.Combobox):
                child.configure(state=combo_state)
            elif isinstance(child, (ttk.Entry, ttk.Button)):
                child.configure(state=state)
            self.set_child_state(child, state, combo_state)

    def convert(self):
        try:
            amount = float(self.amount_var.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid number.")
            return

        if amount <= 0:
            messagebox.showerror("Invalid Amount", "Amount must be greater than zero.")
            return

        from_currency = self.from_var.get()
        to_currency = self.to_var.get()

        if from_currency not in self.rates or to_currency not in self.rates:
            messagebox.showerror(
                "Invalid Currency",
                "Please select supported currency codes.",
            )
            return

        converted_amount = convert_currency(
            amount,
            from_currency,
            to_currency,
            self.rates,
        )
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = (
            f"{timestamp} | {amount:.2f} {from_currency} = "
            f"{converted_amount:.2f} {to_currency}"
        )

        self.result_var.set(
            f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}"
        )
        self.history.append(entry)
        self.history_box.insert(tk.END, entry)
        self.history_box.see(tk.END)
        save_history_entry(entry)

    def swap_currencies(self):
        from_currency = self.from_var.get()
        self.from_var.set(self.to_var.get())
        self.to_var.set(from_currency)


def main():
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
