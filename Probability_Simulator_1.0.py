import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import math
from fractions import Fraction

class ProbabilitySimulator:
    def __init__(self, master):
        self.master = master
        master.title("Probability Simulator")
        master.geometry("600x700")  # Increased height to accommodate new text

        # Event Name
        tk.Label(master, text="Event Name:").grid(row=0, column=0, padx=5, pady=5)
        self.event_name = tk.Entry(master)
        self.event_name.grid(row=0, column=1, padx=5, pady=5)
        self.event_name.insert(0, "Event")

        # Probability
        tk.Label(master, text="Probability (0-1 or fraction):").grid(row=1, column=0, padx=5, pady=5)
        self.probability = tk.Entry(master)
        self.probability.grid(row=1, column=1, padx=5, pady=5)

        # Number of Rolls
        tk.Label(master, text="Number of Rolls:").grid(row=2, column=0, padx=5, pady=5)
        self.num_rolls = tk.Entry(master)
        self.num_rolls.grid(row=2, column=1, padx=5, pady=5)

        # Simulate Button
        self.simulate_button = tk.Button(master, text="Simulate", command=self.simulate)
        self.simulate_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Result Labels
        self.prob_result_label = tk.Label(master, text="")
        self.prob_result_label.grid(row=4, column=0, columnspan=2, pady=5)

        self.occur_result_label = tk.Label(master, text="")
        self.occur_result_label.grid(row=5, column=0, columnspan=2, pady=5)

        # Graph
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master)
        self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def parse_probability(self, prob_str):
        try:
            # Try to parse as a fraction first
            return float(Fraction(prob_str))
        except ValueError:
            # If not a fraction, try to parse as a float
            return float(prob_str)

    def simulate(self):
        try:
            prob = self.parse_probability(self.probability.get())
            rolls = int(self.num_rolls.get())
            event_name = self.event_name.get()

            if not (0 <= prob <= 1):
                raise ValueError("Probability must be between 0 and 1")

            successes = sum(random.random() < prob for _ in range(rolls))
            failures = rolls - successes

            # Calculate probability of at least one success
            prob_at_least_one = 1 - (1 - prob) ** rolls

            # Update result labels
            self.prob_result_label.config(text=f"Probability of at least one {event_name}: {prob_at_least_one:.4f}")
            self.occur_result_label.config(text=f"{event_name} occurred {successes} times and did not occur {failures} times")

            # Update graph
            self.ax.clear()
            self.ax.bar([f"{event_name} Occurred", f"{event_name} Did Not Occur"], [successes, failures])
            self.ax.set_ylabel("Number of Occurrences")
            self.ax.set_title(f"Simulation Results for {rolls} Rolls")
            self.canvas.draw()

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

root = tk.Tk()
simulator = ProbabilitySimulator(root)
root.mainloop()