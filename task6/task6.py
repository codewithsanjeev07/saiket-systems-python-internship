"""SaiKet Systems — Internship
Task 6: Expert-Level Word Count Tool
- Counts words, lines, characters, sentences, paragraphs
- Word frequency analysis with stop-word filtering
- Readability score (Flesch-Kincaid)
- Rich terminal output + optional JSON/CSV export
- Works on any UTF-8 text file or piped stdin
"""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from word_count_tool import analyze_text, export_csv, export_json, format_score


class WordCountToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expert-Level Word Count Tool")
        self.root.geometry("1040x720")
        self.root.minsize(900, 620)

        self.current_source = "typed text"
        self.current_analysis = None

        self.include_stop_words_var = tk.BooleanVar(value=False)
        self.top_limit_var = tk.StringVar(value="10")
        self.status_var = tk.StringVar(value="Paste text or open a UTF-8 file.")

        self.metric_vars = {
            "words": tk.StringVar(value="0"),
            "lines": tk.StringVar(value="0"),
            "characters": tk.StringVar(value="0"),
            "characters_no_spaces": tk.StringVar(value="0"),
            "sentences": tk.StringVar(value="0"),
            "paragraphs": tk.StringVar(value="0"),
            "flesch_reading_ease": tk.StringVar(value="N/A"),
            "flesch_kincaid_grade": tk.StringVar(value="N/A"),
        }

        self.build_ui()

    def build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main = ttk.Frame(self.root, padding=18)
        main.grid(row=0, column=0, sticky="nsew")
        main.columnconfigure(0, weight=1)
        main.rowconfigure(2, weight=1)

        header = ttk.Frame(main)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        ttk.Label(
            header,
            text="Expert-Level Word Count Tool",
            font=("Segoe UI", 18, "bold"),
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            header,
            text="Analyze UTF-8 files or pasted text with counts, readability, and word frequency.",
        ).grid(row=1, column=0, sticky="w", pady=(4, 14))

        actions = ttk.Frame(header)
        actions.grid(row=0, column=1, rowspan=2, sticky="e")

        ttk.Button(actions, text="Open File", command=self.open_file).grid(
            row=0,
            column=0,
            padx=(0, 8),
        )
        ttk.Button(actions, text="Analyze", command=self.analyze_current_text).grid(
            row=0,
            column=1,
            padx=(0, 8),
        )
        ttk.Button(actions, text="Clear", command=self.clear_text).grid(
            row=0,
            column=2,
        )

        options = ttk.Frame(main)
        options.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        options.columnconfigure(6, weight=1)

        ttk.Label(options, text="Top words").grid(row=0, column=0, sticky="w")
        ttk.Spinbox(
            options,
            from_=1,
            to=100,
            textvariable=self.top_limit_var,
            width=6,
        ).grid(row=0, column=1, sticky="w", padx=(8, 18))

        ttk.Checkbutton(
            options,
            text="Include stop words",
            variable=self.include_stop_words_var,
        ).grid(row=0, column=2, sticky="w")

        ttk.Button(options, text="Export JSON", command=self.export_as_json).grid(
            row=0,
            column=3,
            padx=(18, 8),
        )
        ttk.Button(options, text="Export CSV", command=self.export_as_csv).grid(
            row=0,
            column=4,
            padx=(0, 8),
        )
        ttk.Button(
            options,
            text="Copy Report",
            command=self.copy_report_to_clipboard,
        ).grid(
            row=0,
            column=5,
        )

        ttk.Label(options, textvariable=self.status_var).grid(
            row=0,
            column=6,
            sticky="e",
        )

        workspace = ttk.PanedWindow(main, orient="horizontal")
        workspace.grid(row=2, column=0, sticky="nsew")

        editor_frame = ttk.LabelFrame(workspace, text="Input Text", padding=8)
        editor_frame.columnconfigure(0, weight=1)
        editor_frame.rowconfigure(0, weight=1)

        self.text_box = tk.Text(editor_frame, wrap="word", undo=True)
        self.text_box.grid(row=0, column=0, sticky="nsew")

        text_scroll = ttk.Scrollbar(
            editor_frame,
            orient="vertical",
            command=self.text_box.yview,
        )
        text_scroll.grid(row=0, column=1, sticky="ns")
        self.text_box.configure(yscrollcommand=text_scroll.set)

        results_frame = ttk.Frame(workspace)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(2, weight=1)

        metrics_frame = ttk.LabelFrame(results_frame, text="Counts and Readability", padding=10)
        metrics_frame.grid(row=0, column=0, sticky="ew")
        metrics_frame.columnconfigure((1, 3), weight=1)

        metrics = [
            ("Words", "words"),
            ("Lines", "lines"),
            ("Characters", "characters"),
            ("Characters no spaces", "characters_no_spaces"),
            ("Sentences", "sentences"),
            ("Paragraphs", "paragraphs"),
            ("Flesch Reading Ease", "flesch_reading_ease"),
            ("Flesch-Kincaid Grade", "flesch_kincaid_grade"),
        ]

        for index, (label, key) in enumerate(metrics):
            row = index // 2
            column = (index % 2) * 2
            ttk.Label(metrics_frame, text=label).grid(
                row=row,
                column=column,
                sticky="w",
                pady=3,
            )
            ttk.Label(
                metrics_frame,
                textvariable=self.metric_vars[key],
                font=("Segoe UI", 10, "bold"),
            ).grid(row=row, column=column + 1, sticky="w", padx=(8, 18), pady=3)

        frequency_frame = ttk.LabelFrame(results_frame, text="Word Frequency", padding=8)
        frequency_frame.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        frequency_frame.columnconfigure(0, weight=1)
        frequency_frame.rowconfigure(0, weight=1)

        self.frequency_table = ttk.Treeview(
            frequency_frame,
            columns=("word", "count"),
            show="headings",
            height=10,
        )
        self.frequency_table.heading("word", text="Word")
        self.frequency_table.heading("count", text="Count")
        self.frequency_table.column("word", width=220, anchor="w")
        self.frequency_table.column("count", width=90, anchor="center")
        self.frequency_table.grid(row=0, column=0, sticky="nsew")

        frequency_scroll = ttk.Scrollbar(
            frequency_frame,
            orient="vertical",
            command=self.frequency_table.yview,
        )
        frequency_scroll.grid(row=0, column=1, sticky="ns")
        self.frequency_table.configure(yscrollcommand=frequency_scroll.set)

        report_frame = ttk.LabelFrame(results_frame, text="Report", padding=8)
        report_frame.grid(row=2, column=0, sticky="nsew", pady=(12, 0))
        report_frame.columnconfigure(0, weight=1)
        report_frame.rowconfigure(0, weight=1)

        self.report_box = tk.Text(report_frame, height=8, wrap="word")
        self.report_box.grid(row=0, column=0, sticky="nsew")
        self.report_box.configure(state="disabled")

        report_scroll = ttk.Scrollbar(
            report_frame,
            orient="vertical",
            command=self.report_box.yview,
        )
        report_scroll.grid(row=0, column=1, sticky="ns")
        self.report_box.configure(yscrollcommand=report_scroll.set)

        workspace.add(editor_frame, weight=3)
        workspace.add(results_frame, weight=2)

        self.root.bind("<Control-o>", lambda _event: self.open_file())
        self.root.bind("<Control-s>", lambda _event: self.export_as_json())
        self.root.bind("<F5>", lambda _event: self.analyze_current_text())

    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Open UTF-8 text file",
            filetypes=[
                ("Text files", "*.txt *.md *.csv *.json *.py *.log"),
                ("All files", "*.*"),
            ],
        )
        if not file_path:
            return

        try:
            text = Path(file_path).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            messagebox.showerror("Open Error", "The selected file is not valid UTF-8.")
            return
        except OSError as error:
            messagebox.showerror("Open Error", f"Could not open file.\n\n{error}")
            return

        self.current_source = file_path
        self.text_box.delete("1.0", tk.END)
        self.text_box.insert("1.0", text)
        self.status_var.set(f"Loaded {Path(file_path).name}")
        self.analyze_current_text()

    def clear_text(self):
        self.current_source = "typed text"
        self.current_analysis = None
        self.text_box.delete("1.0", tk.END)
        self.reset_results()
        self.status_var.set("Cleared.")

    def validate_top_limit(self):
        try:
            limit = int(self.top_limit_var.get())
        except ValueError:
            messagebox.showerror("Invalid Limit", "Top words must be a whole number.")
            return None

        if limit <= 0:
            messagebox.showerror("Invalid Limit", "Top words must be greater than zero.")
            return None

        return limit

    def analyze_current_text(self):
        limit = self.validate_top_limit()
        if limit is None:
            return

        text = self.text_box.get("1.0", "end-1c")
        self.current_analysis = analyze_text(
            text,
            self.current_source,
            self.include_stop_words_var.get(),
            limit,
        )
        self.update_results(self.current_analysis)
        self.status_var.set("Analysis complete.")

    def reset_results(self):
        for variable in self.metric_vars.values():
            variable.set("0")
        self.metric_vars["flesch_reading_ease"].set("N/A")
        self.metric_vars["flesch_kincaid_grade"].set("N/A")

        for row in self.frequency_table.get_children():
            self.frequency_table.delete(row)

        self.report_box.configure(state="normal")
        self.report_box.delete("1.0", tk.END)
        self.report_box.configure(state="disabled")

    def update_results(self, analysis):
        self.metric_vars["words"].set(str(analysis["words"]))
        self.metric_vars["lines"].set(str(analysis["lines"]))
        self.metric_vars["characters"].set(str(analysis["characters"]))
        self.metric_vars["characters_no_spaces"].set(
            str(analysis["characters_no_spaces"])
        )
        self.metric_vars["sentences"].set(str(analysis["sentences"]))
        self.metric_vars["paragraphs"].set(str(analysis["paragraphs"]))
        self.metric_vars["flesch_reading_ease"].set(
            format_score(analysis["readability"]["flesch_reading_ease"])
        )
        self.metric_vars["flesch_kincaid_grade"].set(
            format_score(analysis["readability"]["flesch_kincaid_grade"])
        )

        for row in self.frequency_table.get_children():
            self.frequency_table.delete(row)
        for word, count in analysis["top_words"]:
            self.frequency_table.insert("", tk.END, values=(word, count))

        self.report_box.configure(state="normal")
        self.report_box.delete("1.0", tk.END)
        self.report_box.insert("1.0", self.build_report_text(analysis))
        self.report_box.configure(state="disabled")

    def build_report_text(self, analysis):
        readability = analysis["readability"]
        report = [
            "Word Count Tool Report",
            "=" * 44,
            f"Source: {analysis['source']}",
            f"Words: {analysis['words']}",
            f"Lines: {analysis['lines']}",
            f"Characters: {analysis['characters']}",
            f"Characters without spaces: {analysis['characters_no_spaces']}",
            f"Sentences: {analysis['sentences']}",
            f"Paragraphs: {analysis['paragraphs']}",
            "-" * 44,
            "Readability",
            "Flesch Reading Ease: "
            f"{format_score(readability['flesch_reading_ease'])}",
            "Flesch-Kincaid Grade: "
            f"{format_score(readability['flesch_kincaid_grade'])}",
            "-" * 44,
            "Top Words",
        ]

        if analysis["top_words"]:
            report.extend(f"{word:<20} {count}" for word, count in analysis["top_words"])
        else:
            report.append("No words found.")

        return "\n".join(report)

    def require_analysis(self):
        if self.current_analysis is not None:
            return True
        messagebox.showwarning("No Analysis", "Analyze text before exporting.")
        return False

    def export_as_json(self):
        if not self.require_analysis():
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Save JSON export",
        )
        if not output_path:
            return

        try:
            export_json(self.current_analysis, output_path)
            messagebox.showinfo("Export Complete", f"JSON saved to:\n{output_path}")
        except SystemExit as error:
            messagebox.showerror("Export Error", str(error))

    def export_as_csv(self):
        if not self.require_analysis():
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save CSV export",
        )
        if not output_path:
            return

        try:
            export_csv(self.current_analysis, output_path)
            messagebox.showinfo("Export Complete", f"CSV saved to:\n{output_path}")
        except SystemExit as error:
            messagebox.showerror("Export Error", str(error))

    def copy_report_to_clipboard(self):
        if not self.require_analysis():
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.build_report_text(self.current_analysis))
        self.status_var.set("Report copied to clipboard.")


def main():
    root = tk.Tk()
    WordCountToolApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()