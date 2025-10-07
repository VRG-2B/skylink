import os
import random
import time
import math

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def main():
    # Get terminal size
    try:
        terminal_width = os.get_terminal_size().columns
        terminal_height = os.get_terminal_size().lines
    except OSError:
        terminal_width = 80
        terminal_height = 24

    # Initialize snowflakes (each is [x, y, phase])
    snowflakes = []
    snow_density = 3  # Number of new snowflakes per frame
    snow_chars = ['❄', '❅', '❆', '*', '·']  # Different snowflake characters
    # Pink color code
    PINK_COLOR = '\033[95m'
    time_passed = 0

    print("\033[?25l")  # Hide cursor
    try:
        while True:
            # Create new snowflakes
            for _ in range(snow_density):
                if random.random() < 0.4:  # 40% chance to create a new snowflake
                    snowflakes.append([
                        random.randint(0, terminal_width - 1),  # x position
                        0,  # y position
                        random.random() * 2 * math.pi  # phase for swaying
                    ])

            # Clear screen and prepare new frame
            clear_screen()
            
            # Create empty frame
            frame = [[' ' for _ in range(terminal_width)] for _ in range(terminal_height)]
            
            # Update snowflakes and add them to frame
            new_snowflakes = []
            time_passed += 0.1
            
            for flake in snowflakes:
                # Add gentle swaying motion
                flake[0] += math.sin(flake[2] + time_passed) * 0.3
                flake[1] += 0.5  # Move down slower than rain
                
                # Keep snowflake within screen bounds
                x = int(round(flake[0])) % terminal_width
                y = int(round(flake[1]))
                
                if y < terminal_height:
                    if 0 <= x < terminal_width:
                        frame[y][x] = random.choice(snow_chars)
                    new_snowflakes.append(flake)
            
            snowflakes = new_snowflakes
            
            # Print frame with background color
            print('\033[H', end='')  # Move cursor to top-left
            print('\033[44m', end='')  # Set background color
            
            # Print each row with pink snowflakes
            for row in frame:
                line = ''
                for char in row:
                    if char != ' ':
                        line += f"{PINK_COLOR}{char}\033[0m\033[44m"  # Pink color, then reset, then restore background
                    else:
                        line += ' '  # Empty space
                print(line)
            
            # Control animation speed
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\033[?25h")  # Show cursor again
        print("\033[0m")  # Reset all colors
        print("\nSnowfall stopped. Goodbye!")

if __name__ == "__main__":
    # Clear the screen and set background before starting
    print("\033[2J\033[H\033[44m", end='')
    main()