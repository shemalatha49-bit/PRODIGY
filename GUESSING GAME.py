"""
Number Guessing Game
A simple interactive game where the player tries to guess a randomly generated number.
"""

import random


def get_valid_input(prompt):
    """
    Prompt the user for input and validate that it's a valid integer.
    
    Args:
        prompt (str): The message to display to the user
    
    Returns:
        int: A valid integer input from the user
    """
    while True:
        try:
            # Attempt to convert user input to an integer
            user_input = int(input(prompt))
            return user_input
        except ValueError:
            # Handle non-numeric input
            print("Invalid input! Please enter a valid number.")


def play_game(min_range=1, max_range=100):
    """
    Main game logic for the number guessing game.
    
    Args:
        min_range (int): Minimum number in the range (default: 1)
        max_range (int): Maximum number in the range (default: 100)
    """
    # Generate a random number within the specified range
    secret_number = random.randint(min_range, max_range)
    
    # Initialize attempt counter
    attempts = 0
    
    # Display welcome message and game instructions
    print("\n" + "="*50)
    print("Welcome to the Number Guessing Game!")
    print("="*50)
    print(f"I'm thinking of a number between {min_range} and {max_range}.")
    print("Try to guess it!\n")
    
    # Main game loop - continues until the user guesses correctly
    while True:
        # Get user's guess (with input validation)
        guess = get_valid_input("Enter your guess: ")
        
        # Increment attempt counter
        attempts += 1
        
        # Compare guess with the secret number and provide feedback
        if guess < secret_number:
            print("Too low! Try again.\n")
        elif guess > secret_number:
            print("Too high! Try again.\n")
        else:
            # Correct guess - exit the loop
            break
    
    # Display congratulatory message with attempt count
    print("\n" + "="*50)
    print(f"🎉 Congratulations! You guessed the number in {attempts} attempt{'s' if attempts != 1 else ''}!")
    print("="*50)


def main():
    """
    Main function to run the game and handle replay functionality.
    """
    while True:
        # Play one round of the game
        play_game()
        
        # Ask if the user wants to play again
        play_again = input("\nWould you like to play again? (yes/no): ").lower().strip()
        
        if play_again not in ['yes', 'y']:
            print("\nThanks for playing! Goodbye! 👋")
            break


# Entry point of the program
if __name__ == "__main__":
    main()
