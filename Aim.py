import tkinter as tk
import random

# Constants
WIDTH, HEIGHT = 600, 500  # Larger window
CIRCLE_RADIUS = 20
GAME_DURATION = 30  # 30-second timer
COUNTDOWN_DURATION = 3  # 3-second countdown

# Initialize score, timer, and high score
score = 0
time_left = GAME_DURATION
high_score = 0
countdown = COUNTDOWN_DURATION
difficulty = "Easy"  # Default difficulty
circle_move_job = None  # To track the scheduled circle movement

def move_circle():
    """Move the circle to a new random position based on the difficulty."""
    global circle_move_job
    new_x = random.randint(CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS)
    new_y = random.randint(CIRCLE_RADIUS, HEIGHT - CIRCLE_RADIUS)
    canvas.coords(circle, new_x - CIRCLE_RADIUS, new_y - CIRCLE_RADIUS, new_x + CIRCLE_RADIUS, new_y + CIRCLE_RADIUS)
    # Reschedule the circle movement based on difficulty
    if difficulty == "Medium":
        circle_move_job = root.after(1500, move_circle)  # Move every 1 second
    elif difficulty == "Hard":
        circle_move_job = root.after(750, move_circle)  # Move every 0.5 seconds

def on_circle_click(event):
    """Handle circle click events, update the score, and reset the movement timer."""
    global score, circle_move_job
    circle_x1, circle_y1, circle_x2, circle_y2 = canvas.coords(circle)
    if (circle_x1 <= event.x <= circle_x2) and (circle_y1 <= event.y <= circle_y2):
        score += 1  # Increment score
        score_label.config(text=f"Score: {score}")  # Update score display
        if difficulty != "Easy":
            # Cancel the previous movement timer and restart it
            if circle_move_job:
                root.after_cancel(circle_move_job)
            move_circle()  # Reset the movement timer

def update_timer():
    """Update the game timer and end the game if time runs out."""
    global time_left
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time Left: {time_left}s")
        root.after(1000, update_timer)  # Update every second
    else:
        end_game()

def start_countdown():
    """Start the 3-second countdown before the game begins."""
    global countdown
    if countdown > 0:
        countdown_label.config(text=f"Starting in: {countdown}")
        countdown -= 1
        root.after(1000, start_countdown)  # Update every second
    else:
        countdown_label.config(text="Go!")
        root.after(500, lambda: countdown_label.config(text=""))  # Clear "Go!" after 0.5 seconds
        canvas.bind("<Button-1>", on_circle_click)  # Enable clicking
        if difficulty != "Easy":
            move_circle()  # Start moving the circle for Medium and Hard modes
        update_timer()  # Start the game timer

def start_game():
    """Start the game by hiding the play button and starting the countdown."""
    global score, time_left, countdown, circle_move_job
    score = 0
    time_left = GAME_DURATION
    countdown = COUNTDOWN_DURATION
    score_label.config(text=f"Score: {score}")
    timer_label.config(text=f"Time Left: {time_left}s")
    play_button.pack_forget()  # Hide the play button
    start_countdown()  # Start the 3-second countdown

def end_game():
    """End the game and display the final score, high score, and a 'Play Again' button."""
    global high_score, circle_move_job
    canvas.unbind("<Button-1>")  # Disable clicking
    timer_label.config(text="Time's up!")
    final_score_label.config(text=f"Final Score: {score}", font=("Arial", 20))
    
    # Update high score if the current score is higher
    if score > high_score:
        high_score = score
        high_score_label.config(text=f"HS: {high_score}", fg="red")  # Update high score display
    
    # Cancel any pending circle movement
    if circle_move_job:
        root.after_cancel(circle_move_job)
    play_again_button.pack()  # Show the "Play Again" button

def reset_game():
    """Reset the game to its initial state."""
    global score, time_left, countdown, circle_move_job
    score = 0
    time_left = GAME_DURATION
    countdown = COUNTDOWN_DURATION
    score_label.config(text=f"Score: {score}")
    timer_label.config(text=f"Time Left: {time_left}s")
    final_score_label.config(text="")
    play_again_button.pack_forget()  # Hide the "Play Again" button
    play_button.pack()  # Show the "Play" button
    # Move the circle to a new random position
    new_x = random.randint(CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS)
    new_y = random.randint(CIRCLE_RADIUS, HEIGHT - CIRCLE_RADIUS)
    canvas.coords(circle, new_x - CIRCLE_RADIUS, new_y - CIRCLE_RADIUS, new_x + CIRCLE_RADIUS, new_y + CIRCLE_RADIUS)
    # Cancel any pending circle movement
    if circle_move_job:
        root.after_cancel(circle_move_job)

def set_difficulty():
    """Update the difficulty based on the selected radio button."""
    global difficulty
    difficulty = difficulty_var.get()
    difficulty_label.config(text=f"Difficulty: {difficulty}")

# Create the main window
root = tk.Tk()
root.title("Timed Click-the-Circle Game")

# Create a canvas widget
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# Create a label to display the score
score_label = tk.Label(root, text=f"Score: {score}", font=("Arial", 16))
score_label.pack()

# Create a label to display the timer
timer_label = tk.Label(root, text=f"Time Left: {time_left}s", font=("Arial", 16))
timer_label.pack()

# Create a label to display the countdown
countdown_label = tk.Label(root, text="", font=("Arial", 20))
countdown_label.pack()

# Create a label to display the final score
final_score_label = tk.Label(root, text="", font=("Arial", 20))
final_score_label.pack()

# Create a label to display the high score (positioned in the bottom-right corner)
high_score_label = tk.Label(root, text=f"HS: {high_score}", font=("Arial", 16, "bold"), fg="red", bg="white")
high_score_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)  # Bottom-right corner with padding

# Create a "Play" button
play_button = tk.Button(root, text="Play", font=("Arial", 16), command=start_game)
play_button.pack()

# Create a "Play Again" button (initially hidden)
play_again_button = tk.Button(root, text="Play Again", font=("Arial", 16), command=reset_game)

# Create a frame to hold the radio buttons
difficulty_frame = tk.Frame(root)
difficulty_frame.pack()

# Create a label for the difficulty selection
difficulty_label = tk.Label(difficulty_frame, text="Difficulty: Easy", font=("Arial", 14))
difficulty_label.pack(side="left")

# Create a variable to store the selected difficulty
difficulty_var = tk.StringVar(value="Easy")  # Default difficulty

# Create radio buttons for each difficulty level
easy_radio = tk.Radiobutton(difficulty_frame, text="Easy", variable=difficulty_var, value="Easy", font=("Arial", 12), command=set_difficulty)
easy_radio.pack(side="left")

medium_radio = tk.Radiobutton(difficulty_frame, text="Medium", variable=difficulty_var, value="Medium", font=("Arial", 12), command=set_difficulty)
medium_radio.pack(side="left")

hard_radio = tk.Radiobutton(difficulty_frame, text="Hard", variable=difficulty_var, value="Hard", font=("Arial", 12), command=set_difficulty)
hard_radio.pack(side="left")

# Initial random position for the circle
start_x = random.randint(CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS)
start_y = random.randint(CIRCLE_RADIUS, HEIGHT - CIRCLE_RADIUS)

# Draw the circle
circle = canvas.create_oval(
    start_x - CIRCLE_RADIUS, start_y - CIRCLE_RADIUS,
    start_x + CIRCLE_RADIUS, start_y + CIRCLE_RADIUS,
    fill="blue", outline="black"
)

# Start the Tkinter event loop
root.mainloop()