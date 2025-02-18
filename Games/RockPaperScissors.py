import random

# Define choices
choices = {"1": "✊", "2": "✋", "3": "✌️"}
point = 10

def main():
    global point
    print("Welcome to Rock-Paper-Scissors! Earn points by winning rounds.")

    while point > 0:
        print("\n--------------------")
        print("|1. ✊ - Rock      |")
        print("|2. ✋ - Paper     |")
        print("|3. ✌️  - Scissors  |")
        print("|4. ❌ - Quit      |")
        print("--------------------")

        user_input = input("Choose your number (1-3) or 4 to quit: ").strip()

        if user_input == "4":
            print("Thanks for playing! Final Score:", point)
            break

        if user_input not in choices:
            print("Invalid input, please enter a number between 1 and 3.")
            continue

        user_choice = choices[user_input]
        #computer_choice = random.choice(list(choices.values()))
        computer_choice = biased_computer_choice(user_input)
        result = determine_winner(user_choice, computer_choice)

        update_score(result)
        print("------------------------------------------")
        print(f"{user_choice} vs {computer_choice}. You {result}!")
        print(f"Your current points: {point}")
        print("------------------------------------------")

    print("\n*****************************************")
    print("Game Over. Your final score is:", point)
    print("*****************************************")

def biased_computer_choice(user_input):
    """Makes the AI favor the winning choice slightly more often."""
    #weights = {"1": [0.2, 0.5, 0.3],  # User chose Rock -> AI favors Paper
    #           "2": [0.3, 0.2, 0.5],  # User chose Paper -> AI favors Scissors
    #           "3": [0.5, 0.3, 0.2]}  # User chose Scissors -> AI favors Rock
    weights = {"1": [0.3, 0.3, 0.4],  # User chose Rock -> AI favors Scissors
               "2": [0.4, 0.3, 0.3],  # User chose Paper -> AI favors Rock
               "3": [0.3, 0.4, 0.3]}  # User chose Scissors -> AI favors Paper
    return random.choices(list(choices.values()), weights=weights[user_input])[0]

def determine_winner(user, computer):
    """Determines the winner based on choices."""
    outcomes = {
        ("✊", "✌️"): "Win",  ("✊", "✋"): "Loss",  ("✊", "✊"): "Tie",
        ("✋", "✊"): "Win",  ("✋", "✌️"): "Loss",  ("✋", "✋"): "Tie",
        ("✌️", "✋"): "Win",  ("✌️", "✊"): "Loss",  ("✌️", "✌️"): "Tie"
    }
    return outcomes[(user, computer)]

def update_score(result):
    """Updates the player's points based on the result."""
    global point
    if result == "Win":
        point += 2
    elif result == "Loss":
        point -= 2
    else:  # Tied
        point -= 0

if __name__ == "__main__":
    main()
