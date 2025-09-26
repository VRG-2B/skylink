import random

def number_guessing_game():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    
    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10
    
    while attempts < max_attempts:
        # Get player's guess
        try:
            guess = int(input(f"\nYou have {max_attempts - attempts} attempts left. Enter your guess: "))
        except ValueError:
            print("Please enter a valid number!")
            continue
            
        attempts += 1
        
        # Check the guess
        if guess < 1 or guess > 100:
            print("Please guess a number between 1 and 100!")
            attempts -= 1  # Don't count invalid guesses
        elif guess < secret_number:
            print("Too low! Try a higher number.")
        elif guess > secret_number:
            print("Too high! Try a lower number.")
        else:
            print(f"\nCongratulations! You've guessed the number {secret_number} correctly!")
            print(f"It took you {attempts} attempts.")
            break
    
    # If player runs out of attempts
    if attempts == max_attempts and guess != secret_number:
        print(f"\nGame Over! The number was {secret_number}.")
    
    # Ask to play again
    play_again = input("\nWould you like to play again? (yes/no): ")
    if play_again.lower() == 'yes':
        number_guessing_game()

if __name__ == "__main__":
    try:
        number_guessing_game()
        print("\nThanks for playing!")
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
