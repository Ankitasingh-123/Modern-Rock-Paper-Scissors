import tkinter as tk
import random

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("600x600")
root.resizable(False, False)

# ---------------- GAME VARIABLES ----------------
choices = ["Rock", "Paper", "Scissors"]
user_score = 0
computer_score = 0
round_count = 0
max_rounds = 5
game_over = False

# ---------------- GRADIENT BACKGROUND ----------------
canvas = tk.Canvas(root, width=600, height=600, highlightthickness=0)
canvas.pack(fill="both", expand=True)

for i in range(600):
    r = int(15 + (i/600)*50)
    g = int(15 + (i/600)*50)
    b = int(40 + (i/600)*90)
    color = f'#{r:02x}{g:02x}{b:02x}'
    canvas.create_line(0, i, 600, i, fill=color)

# ---------------- TITLE ----------------
title = tk.Label(root,
                 text="🎮 ROCK PAPER SCISSORS-AB AAYEGA MJA",
                 font=("Segoe UI", 22, "bold"),
                 fg="white",
                 bg="#141428")
title.place(relx=0.5, y=50, anchor="center")

# ---------------- RESULT LABEL ----------------
result_label = tk.Label(root,
                        text="First to 3 wins 🏆",
                        font=("Segoe UI", 14),
                        fg="#dddddd",
                        bg="#141428",
                        justify="center")
result_label.place(relx=0.5, y=110, anchor="center")

# ---------------- SCORE LABEL ----------------
score_label = tk.Label(root,
                       text="You: 0   Computer: 0   Round: 0/5",
                       font=("Segoe UI", 12, "bold"),
                       fg="white",
                       bg="#141428")
score_label.place(relx=0.5, y=150, anchor="center")

# ---------------- ANIMATION EFFECT ----------------
def flash_result(text, color):
    result_label.config(text=text, fg=color)
    root.after(300, lambda: result_label.config(fg="white"))

# ---------------- GAME LOGIC ----------------
def play(user_choice):
    global user_score, computer_score, round_count, game_over

    if game_over:
        return

    computer_choice = random.choice(choices)
    round_count += 1

    if user_choice == computer_choice:
        flash_result(f"Tie! 🤝 You both chose {user_choice}", "#ffaa00")

    elif (
        (user_choice == "Rock" and computer_choice == "Scissors") or
        (user_choice == "Paper" and computer_choice == "Rock") or
        (user_choice == "Scissors" and computer_choice == "Paper")
    ):
        user_score += 1
        flash_result(f"You Win! 🎉 {user_choice} beats {computer_choice}", "#00ff88")

    else:
        computer_score += 1
        flash_result(f"You Lose! 😢 {computer_choice} beats {user_choice}", "#ff4c4c")

    score_label.config(
        text=f"You: {user_score}   Computer: {computer_score}   Round: {round_count}/5"
    )

    if user_score == 3 or computer_score == 3 or round_count == max_rounds:
        end_game()

# ---------------- END GAME ----------------
def end_game():
    global game_over
    game_over = True

    if user_score > computer_score:
        result_label.config(text="🏆 YOU WON THE MATCH!", fg="#00ff88")
    elif computer_score > user_score:
        result_label.config(text="💀 COMPUTER WON THE MATCH!", fg="#ff4c4c")
    else:
        result_label.config(text="🤝 MATCH DRAW!", fg="#ffaa00")

    disable_buttons()

# ---------------- RESET ----------------
def reset_game():
    global user_score, computer_score, round_count, game_over
    user_score = 0
    computer_score = 0
    round_count = 0
    game_over = False

    result_label.config(text="First to 3 wins 🏆", fg="white")
    score_label.config(text="You: 0   Computer: 0   Round: 0/5")
    enable_buttons()

# ---------------- BUTTON CONTROL ----------------
def disable_buttons():
    rock_btn.disable()
    paper_btn.disable()
    scissor_btn.disable()

def enable_buttons():
    rock_btn.enable()
    paper_btn.enable()
    scissor_btn.enable()

# ---------------- CUSTOM ROUNDED BUTTON ----------------
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, color):
        super().__init__(parent, width=170, height=55,
                         bg="#141428", highlightthickness=0)
        self.command = command
        self.color = color
        self.active = True

        self.rect = self.create_oval(5, 5, 165, 50, fill=color, outline="")
        self.label = self.create_text(85, 28,
                                      text=text,
                                      fill="white",
                                      font=("Segoe UI", 12, "bold"))

        self.bind("<Button-1>", self.click)
        self.bind("<Enter>", self.hover)
        self.bind("<Leave>", self.leave)

    def click(self, event):
        if self.active:
            self.command()

    def hover(self, event):
        if self.active:
            self.itemconfig(self.rect, fill="white")
            self.itemconfig(self.label, fill=self.color)

    def leave(self, event):
        if self.active:
            self.itemconfig(self.rect, fill=self.color)
            self.itemconfig(self.label, fill="white")

    def disable(self):
        self.active = False
        self.itemconfig(self.rect, fill="#555555")

    def enable(self):
        self.active = True
        self.itemconfig(self.rect, fill=self.color)

# ---------------- BUTTONS ----------------
rock_btn = RoundedButton(root, "🪨 Rock", lambda: play("Rock"), "#ff4c4c")
rock_btn.place(relx=0.2, rely=0.65, anchor="center")

paper_btn = RoundedButton(root, "📄 Paper", lambda: play("Paper"), "#4c8cff")
paper_btn.place(relx=0.5, rely=0.65, anchor="center")

scissor_btn = RoundedButton(root, "✂ Scissors", lambda: play("Scissors"), "#00c853")
scissor_btn.place(relx=0.8, rely=0.65, anchor="center")

reset_btn = RoundedButton(root, "🔄 Reset", reset_game, "#ffaa00")
reset_btn.place(relx=0.5, rely=0.8, anchor="center")

root.mainloop()