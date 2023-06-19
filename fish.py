#!/bin/python3

'''
Somewhat inspired by https://pypi.org/project/fish/
'''

import time
import curses
from random import randint, choice

stdscr = curses.initscr()

height = curses.LINES
width  = curses.COLS

# This is easiest, since we don't just want to reverse
arts_r = ["><}}}*>", ">))'>", "><))))°>"]
arts_l = ["<*{{{><", "<'((<", "<°((((><"]

class Fish():
    __slot__ = ["x", "y", "color", "is_left", "speed", "art_l", "art_r"]

    def __init__(self):
        # Bottom 3 are reserved for "rocks"
        self.x = randint(1, width-1)
        self.y = randint(1, height-4)
       
        # Color number is a color pair number
        self.color = randint(0, 7)

        self.is_left = randint(0,1)==1
        self.speed = randint(1, 3)

        # Pick type of fish
        art_index = randint(0,len(arts_r)-1)
        self.art_l = arts_l[art_index]
        self.art_r = arts_r[art_index]

        self.l = len(self.art_l)

    def erase(self):
        # If user resizes window, addstr can throw an exception
        try:
            stdscr.addstr(self.y, self.x, " "*(self.l+1))
        except curses.error:
            pass

    def display(self):
        c = curses.color_pair(self.color) | curses.A_BOLD

        # If user resizes window, addstr can throw an exception
        try:
            if self.is_left:
                stdscr.addstr(self.y, self.x, self.art_l, c)
            else:
                stdscr.addstr(self.y, self.x, self.art_r, c)
        except curses.error:
            pass

    def act(self):
        # Undraw fish
        self.erase()

        # Check left/right wall collision
        if self.x >= width-self.speed-self.l or self.x <= self.speed:
            if not self.is_left:
                self.x -= self.speed
            self.is_left = not self.is_left

        # Move
        if self.is_left:
            self.x -= self.speed
        else:
            self.x += self.speed

        
        # Randomly move up/down
        if randint(0,20) == 3:
            if randint(0,1) == 1:
                self.y -= 1
            else:
                self.y += 1

        # Bounds checks for y
        if self.y < 3:
            self.y = 3
        elif self.y > height-4:
            self.y = height-4

        # Print fish
        self.display()

def init_rocks():
    # Randomly generate rocks
    rock_t = ["0", "o", "O", "&", "@"]
    rocks = ""
    for i in range(width-1):
        rocks += choice(rock_t)
    return rocks

def draw_rocks(rock, line):
    # Draw rock line
    stdscr.addstr(line, 0, rock, curses.color_pair(9))

def init_weeds():
    weeds = [randint(10, width-10) for i in range(int(width/30))]
    return weeds

def draw_weeds(weeds, i):
    for weed in weeds:
        draw_weed(weed, i)

def draw_weed(x, i):
    try:
        b = int(i/20)%2==1
        for i in range(3, 8):
            if b:
                stdscr.addstr(height-i, x, "(( ", curses.color_pair(2))
            else:
                stdscr.addstr(height-i, x, " ))", curses.color_pair(2))
            b = not b
    except E:
        pass

def main():
    curses.noecho()
    curses.curs_set(False)
    curses.start_color()

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(9, curses.COLOR_MAGENTA, curses.COLOR_BLUE)

    stdscr.bkgd(' ', curses.color_pair(1))

    fishes = [Fish() for i in range(int(width*height / 150))]

    weeds = init_weeds()

    rocks = [init_rocks() for i in range(3)]

    i = 0
    while True:
        draw_weeds(weeds, i)
        i+=1

        # Draw rocks (pink at bottom)
        draw_rocks(rocks[0], height-1)
        draw_rocks(rocks[1], height-2)
        draw_rocks(rocks[2], height-3)

        # Draw all fish
        for fish in fishes:
            fish.act()

        # Show changes
        stdscr.refresh()

        time.sleep(.12)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, Exception) as e:
        curses.endwin()
