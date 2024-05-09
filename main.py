import curses
import queue
import time
from curses import wrapper

maze = [["#", "O", "#", "#", "#", "#", "#", "#", "#"],
        ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
        ["#", " ", "#", "#", "#", " ", "#", " ", "#"],
        ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
        ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
        ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
        ["#", "#", "#", "#", "#", "#", "#", "X", "#"]]


def print_maze(maze, stdscr, path=[]):
  BLUE = curses.color_pair(1)
  RED = curses.color_pair(2)

  for i, row in enumerate(maze):
    for j, value in enumerate(row):
      if (i, j) in path:
        stdscr.addstr(i, j * 2, "x", RED)
      else:
        stdscr.addstr(i, j * 2, value, BLUE)


def find_start(maze, start_symbol):
  for i, row in enumerate(maze):
    for j, value in enumerate(row):
      if value == start_symbol:
        return i, j
  return None


def find_path(maze, stdscr):
  start_symbol = "O"
  end = "X"
  start_pos = find_start(maze, start_symbol)
  q = queue.Queue()
  q.put((start_pos, [start_pos]))
  visited = set()

  while not q.empty():
    current_pos, path = q.get()
    row, column = current_pos
    stdscr.clear()
    print_maze(maze, stdscr, path)
    time.sleep(0.3)
    stdscr.refresh()
    if maze[row][column] == end:
      stdscr.getkey()
      return path
    neighbours = find_neighbours(maze, row, column)
    for neighbor in neighbours:
      if neighbor in visited:
        continue
      r, c = neighbor
      if maze[r][c] == "#":
        continue
      new_path = path + [neighbor]
      q.put((neighbor, new_path))
      visited.add(neighbor)


def find_neighbours(maze, row, col):
  neighbours = []
  if row > 0:  #UP
    neighbours.append((row - 1, col))
  if row + 1 < len(maze):  #Down
    neighbours.append((row + 1, col))
  if col > 0:  #Left
    neighbours.append((row, col - 1))
  if col + 1 < len(maze[0]):  #Right
    neighbours.append((row, col + 1))
  return neighbours


def main(stdscr):

  curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

  find_path(maze, stdscr)
  stdscr.getch()


wrapper(main)
