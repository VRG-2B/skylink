import random

def play_guessing_game():
    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 7

    print("Welcome to the Number Guessing Game!")
    print(f"I'm thinking of a number between 1 and 100. You have {max_attempts} attempts.")

    while attempts < max_attempts:
        try:
            # Get player's guess
            guess = int(input("Enter your guess: "))
            attempts += 1

            # Check the guess
            if guess < secret_number:
                print(f"Too low! You have {max_attempts - attempts} attempts left.")
            elif guess > secret_number:
                print(f"Too high! You have {max_attempts - attempts} attempts left.")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts!")
                return True
        except ValueError:
            print("Please enter a valid number!")
            attempts -= 1

    print(f"Game Over! The number was {secret_number}")
    return False

def main():
    while True:
        play_guessing_game()
        play_again = input("Would you like to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()