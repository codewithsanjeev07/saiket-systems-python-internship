"""SaiKet Systems Internship Task 2:Guess the Number Game

Description:
Create a number guessing game where the
program generates a random number, and
the user has to guess it. Provide hints (higher
or lower) based on the user's guesses and
keep track of the number of attempts.
Enhance user interaction with clear
instructions and feedback."""

import random
import tkinter as tk
from tkinter import messagebox, ttk


class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("560x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f7fb")

        self.lowest_number = 1
        self.highest_number = 100
        self.secret_number = None
        self.attempts = 0
        self.game_over = False

        self.guess_var = tk.StringVar()
        self.feedback_var = tk.StringVar()
        self.attempts_var = tk.StringVar()
        self.range_var = tk.StringVar(value="1 - 100")

        self.configure_styles()
        self.create_widgets()
        self.start_new_game()

    def configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("App.TFrame", background="#f4f7fb")
        self.style.configure("Panel.TFrame", background="#ffffff")
        self.style.configure(
            "Title.TLabel",
            background="#f4f7fb",
            foreground="#1f2937",
            font=("Segoe UI", 20, "bold"),
        )
        self.style.configure(
            "Body.TLabel",
            background="#ffffff",
            foreground="#374151",
            font=("Segoe UI", 10),
        )
        self.style.configure(
            "Feedback.TLabel",
            background="#ffffff",
            foreground="#2563eb",
            font=("Segoe UI", 13, "bold"),
        )
        self.style.configure(
            "Attempts.TLabel",
            background="#ffffff",
            foreground="#111827",
            font=("Segoe UI", 11, "bold"),
        )
        self.style.configure("TButton", font=("Segoe UI", 10), padding=(12, 7))
        self.style.configure("TEntry", padding=6)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=24, style="App.TFrame")
        main_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(
            main_frame,
            text="Number Guessing Game",
            style="Title.TLabel",
        )
        title_label.pack(pady=(0, 10))

        instructions = (
            "Guess the hidden number. After every guess, you will get a hint "
            "telling you whether to go higher or lower."
        )
        instruction_label = ttk.Label(
            main_frame,
            text=instructions,
            style="Title.TLabel",
            font=("Segoe UI", 10),
            justify="center",
            wraplength=470,
        )
        instruction_label.pack(pady=(0, 16))

        panel = ttk.Frame(main_frame, padding=22, style="Panel.TFrame")
        panel.pack(fill="both", expand=True)

        settings_frame = ttk.Frame(panel, style="Panel.TFrame")
        settings_frame.pack(fill="x", pady=(0, 18))

        ttk.Label(settings_frame, text="Range", style="Body.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        self.range_box = ttk.Combobox(
            settings_frame,
            textvariable=self.range_var,
            values=("1 - 50", "1 - 100", "1 - 500"),
            state="readonly",
            width=14,
        )
        self.range_box.grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.range_box.bind("<<ComboboxSelected>>", lambda _event: self.start_new_game())

        ttk.Button(
            settings_frame,
            text="New Game",
            command=self.start_new_game,
        ).grid(row=1, column=1, sticky="e", pady=(6, 0))
        settings_frame.columnconfigure(1, weight=1)

        input_frame = ttk.Frame(panel, style="Panel.TFrame")
        input_frame.pack(fill="x", pady=(0, 14))

        ttk.Label(input_frame, text="Your guess", style="Body.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 6)
        )

        self.guess_entry = ttk.Entry(
            input_frame,
            textvariable=self.guess_var,
            width=24,
            font=("Segoe UI", 12),
        )
        self.guess_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10))
        self.guess_entry.bind("<Return>", lambda _event: self.check_guess())

        self.guess_button = ttk.Button(
            input_frame,
            text="Submit Guess",
            command=self.check_guess,
        )
        self.guess_button.grid(row=1, column=1, sticky="e")
        input_frame.columnconfigure(0, weight=1)

        feedback_box = ttk.Frame(panel, padding=14, style="Panel.TFrame")
        feedback_box.pack(fill="x", pady=(0, 14))

        self.feedback_label = ttk.Label(
            feedback_box,
            textvariable=self.feedback_var,
            style="Feedback.TLabel",
            justify="center",
            wraplength=470,
        )
        self.feedback_label.pack(fill="x")

        attempts_label = ttk.Label(
            panel,
            textvariable=self.attempts_var,
            style="Attempts.TLabel",
        )
        attempts_label.pack(anchor="w", pady=(0, 8))

        ttk.Label(panel, text="Guess history", style="Body.TLabel").pack(anchor="w")
        history_frame = ttk.Frame(panel, style="Panel.TFrame")
        history_frame.pack(fill="both", expand=True, pady=(6, 0))

        self.history_list = tk.Listbox(
            history_frame,
            height=8,
            activestyle="none",
            borderwidth=1,
            relief="solid",
            font=("Segoe UI", 10),
        )
        self.history_list.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self.history_list.yview,
        )
        scrollbar.pack(side="right", fill="y")
        self.history_list.configure(yscrollcommand=scrollbar.set)

    def start_new_game(self):
        selected_range = self.range_var.get()
        self.highest_number = int(selected_range.split("-")[1].strip())
        self.secret_number = random.randint(self.lowest_number, self.highest_number)
        self.attempts = 0
        self.game_over = False
        self.guess_var.set("")
        self.feedback_var.set(
            f"I picked a number from {self.lowest_number} to {self.highest_number}."
        )
        self.attempts_var.set("Attempts: 0")
        self.guess_entry.config(state="normal")
        self.guess_button.config(state="normal")
        self.feedback_label.configure(foreground="#2563eb")
        self.history_list.delete(0, tk.END)
        self.guess_entry.focus()

    def check_guess(self):
        if self.game_over:
            return

        guess_text = self.guess_var.get().strip()

        if not guess_text:
            messagebox.showwarning("Missing Guess", "Please enter a number.")
            return

        try:
            guess = int(guess_text)
        except ValueError:
            messagebox.showerror("Invalid Guess", "Please enter a valid whole number.")
            self.guess_var.set("")
            self.guess_entry.focus()
            return

        if guess < self.lowest_number or guess > self.highest_number:
            messagebox.showwarning(
                "Out of Range",
                f"Please enter a number between {self.lowest_number} and "
                f"{self.highest_number}.",
            )
            self.guess_var.set("")
            self.guess_entry.focus()
            return

        self.attempts += 1
        self.attempts_var.set(f"Attempts: {self.attempts}")

        if guess < self.secret_number:
            hint = "Too low. Try a higher number."
            self.feedback_var.set(hint)
            self.feedback_label.configure(foreground="#d97706")
            self.add_history(guess, hint)
        elif guess > self.secret_number:
            hint = "Too high. Try a lower number."
            self.feedback_var.set(hint)
            self.feedback_label.configure(foreground="#dc2626")
            self.add_history(guess, hint)
        else:
            self.feedback_var.set(
                f"Correct! You guessed the number in {self.attempts} attempt(s)."
            )
            self.feedback_label.configure(foreground="#059669")
            self.add_history(guess, "Correct!")
            self.game_over = True
            self.guess_entry.config(state="disabled")
            self.guess_button.config(state="disabled")
            messagebox.showinfo(
                "You Win!",
                f"Great job! The number was {self.secret_number}.\n"
                f"Total attempts: {self.attempts}",
            )

        self.guess_var.set("")
        self.guess_entry.focus()

    def add_history(self, guess, hint):
        self.history_list.insert(tk.END, f"Attempt {self.attempts}: {guess} - {hint}")
        self.history_list.see(tk.END)


def main():
    root = tk.Tk()
    NumberGuessingGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
