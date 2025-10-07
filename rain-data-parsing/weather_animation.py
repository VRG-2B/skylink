import random
import os
import time
from typing import List, Tuple

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

class Snowflake:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.char = '*'

class SnowAnimation:
    def __init__(self, width: int = 40, height: int = 20):
        self.width = width
        self.height = height
        self.snowflakes: List[Snowflake] = []
        self.init_snowflakes()

    def init_snowflakes(self):
        num_flakes = self.width // 4  # Control density of snowflakes
        for _ in range(num_flakes):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.snowflakes.append(Snowflake(x, y))

    def update(self):
        for flake in self.snowflakes:
            # Move down
            flake.y += 1
            # Random horizontal movement
            if random.random() < 0.3:
                flake.x += random.choice([-1, 1])
            
            # Wrap around
            if flake.y >= self.height:
                flake.y = 0
                flake.x = random.randint(0, self.width - 1)
            if flake.x < 0:
                flake.x = self.width - 1
            elif flake.x >= self.width:
                flake.x = 0

    def draw(self):
        # Create empty grid
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Place snowflakes
        for flake in self.snowflakes:
            grid[flake.y][flake.x] = flake.char
        
        # Draw frame
        clear_screen()
        print('╔' + '═' * self.width + '╗')
        for row in grid:
            print('║' + ''.join(row) + '║')
        print('╚' + '═' * self.width + '╝')

def main():
    animation = SnowAnimation()
    try:
        while True:
            animation.update()
            animation.draw()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nAnimation stopped.")

if __name__ == "__main__":
    main()
