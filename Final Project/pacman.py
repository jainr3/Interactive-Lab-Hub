#!/usr/bin/env python
from samplebase import SampleBase
from runtext import RunText
import adafruit_mpu6050, board, math, time, threading
from queue import Queue
from rgbmatrix import graphics

def read_pitch_roll(mpu, mpu_queue):
  while True:
    x_accel, y_accel, z_accel = mpu.acceleration
    x_gyro, y_gyro, z_gyro = mpu.gyro
    #print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (x_accel, y_accel, z_accel))
    #print("Gyro X:%.2f, Y: %.2f, Z: %.2f rad/s" % (x_gyro, y_gyro, z_gyro))

    accXnorm = x_accel / math.sqrt((x_accel * x_accel) + (y_accel * y_accel) + (z_accel * z_accel))
    accYnorm = y_accel / math.sqrt((x_accel * x_accel) + (y_accel * y_accel) + (z_accel * z_accel))

    pitch = math.asin(accXnorm)
    roll = -math.asin(accYnorm / math.cos(pitch))

    #print("Pitch {%.2f} Roll {%.2f}" % (pitch, roll))
    mpu_queue.put((pitch, roll))

def read_volume():
  pass



class MatrixPanel(SampleBase):
  def __init__(self, mpu_queue, *args, **kwargs):
    super(MatrixPanel, self).__init__(*args, **kwargs)
    self.mpu_queue = mpu_queue
    self.game = PacmanGame() # configure this if we want multiple games

  def run(self):
    offset_canvas = self.matrix.CreateFrameCanvas()
    while True:
      # First do the home screen stuff
      self.game.display_home_screen(self, offset_canvas, mpu_queue)
      # When that is done, show the game board
      self.game.init_board(self, offset_canvas)

      while not self.game.game_over:
        # Get the inputs synchronously
        pitch, roll = self.get_mpu_pitch_roll()
        volume_level = self.get_volume_level()

        # Update the game state and screen, every game should have a main function
        self.game.update_game_state(self, offset_canvas, pitch, roll, volume_level)
          
        time.sleep(0.05)
      
      # Game is over; go back to home screen
      self.game = PacmanGame() # reset the game state
    

  def get_mpu_pitch_roll(self):
    return self.mpu_queue.get()
  
  def get_volume_level(self):
    # TODO: from the other thread get the volume level info
    return None


class PacmanGame():
  SCORE_COLOR = (128, 0, 128) # PURPLE
  WALL_COLOR = (25, 25, 166) # BLUE
  FOOD_COLOR = (255, 255, 255) # WHITE
  POWER_PELLETS_COLOR = (255, 0, 0) # RED
  PACMAN_COLOR = (255, 255, 0) # YELLOW 

  #ENEMY_BLINKY_COLOR = (255, 0, 0) # RED
  ENEMY_PINKY_COLOR = (255, 184, 255) # PINK
  ENEMY_INKY_COLOR = (0, 255, 255) # AQUA
  ENEMY_FUNKY_COLOR = (0, 255, 0) # GREEN
  #ENEMY_SUE_COLOR = (128, 0, 128) # PURPLE
  ENEMY_CLYDE_COLOR = (255, 184, 82) # ORANGE
  ENEMY_COLORS = [ENEMY_PINKY_COLOR, ENEMY_INKY_COLOR, ENEMY_FUNKY_COLOR, ENEMY_CLYDE_COLOR]

  #GHOST_BLINKY_COLOR = (255, 127, 127) # LIGHT RED
  GHOST_PINKY_COLOR = (255, 182, 193) # LIGHT PINK
  GHOST_INKY_COLOR = (203, 255, 245) # LIGHT AQUA
  GHOST_FUNKY_COLOR = (144, 238, 144) # LIGHT GREEN
  #GHOST_SUE_COLOR = (203, 195, 227) # LIGHT PURPLE
  GHOST_CLYDE_COLOR = (255, 213, 128) # LIGHT ORANGE
  GHOST_COLORS = [GHOST_PINKY_COLOR, GHOST_INKY_COLOR, GHOST_FUNKY_COLOR, GHOST_CLYDE_COLOR]

  GAME_BOARD_LENGTH = 62 # leave 2 pixel cols on right side for score / lives
  GAME_BOARD_HEIGHT = 32

  PACMAN_BOARD = 'pacman_board_2.txt'

  def __init__(self):
    self.walls, self.food, self.power_pellets, self.blanks, self.pacman_init, self.enemies_init = self.read_board_in(PacmanGame.PACMAN_BOARD)
    self.pacman, self.enemies = self.pacman_init, self.enemies_init
    self.score = 0
    self.lives = 3
    self.ghosts_active = False # the position of ghosts and enemies is tracked by the same self.enemies
    self.ghosts_timesteps_left = -1 # Ghosts timesteps left, only used if ghosts are active
    self.game_over = False

  def display_home_screen(self, matrix_panel, offset_canvas, mpu_queue):
    pacman_corrections_black = {0: [0, 1, 2, 8, 9],
                                1: [0, 1, 9],
                                2: [0, 8, 9],
                                3: [7, 8, 9],
                                4: [6, 7, 8, 9],
                                5: [6, 7, 8, 9],
                                6: [7, 8, 9],
                                7: [0, 8, 9],
                                8: [0, 1, 9],
                                9: [0, 1, 2, 8, 9],
                                10: []}

    for x in range(1, 11):
      for y in range(1, 11):
        offset_canvas.SetPixel(x, y, 255, 255, 0)

    for y, x_vals in pacman_corrections_black.items():
      for x in x_vals:
        offset_canvas.SetPixel(1+x, 1+y, 0, 0, 0)

    heart_corrections_black = {0: [0, 3, 4, 5, 8],
                              1: [4],
                              4: [0, 8],
                              5: [0, 1, 7, 8],
                              6: [0, 1, 2, 6, 7, 8], 
                              7: [0, 1, 2, 3, 5, 6, 7, 8],
                              8: [0, 1, 2, 3, 4, 5, 6, 7, 8]}

    for x in range(15, 24):
      for y in range(23, 32):
        offset_canvas.SetPixel(x, y, 255, 0, 0)

    for y, x_vals in heart_corrections_black.items():
      for x in x_vals:
        offset_canvas.SetPixel(15+x, 23+y, 0, 0, 0)

    font = graphics.Font()
    font.LoadFont("fonts/4x6.bdf")
    textColor = graphics.Color(255, 255, 255)
    pos = offset_canvas.width
    my_text = "3x"
    len = graphics.DrawText(offset_canvas, font, 4, 30, textColor, my_text)

    my_text = "TILT"
    len = graphics.DrawText(offset_canvas, font, 12, 21, textColor, my_text)

    arrow_corrections_black = {0: [0, 1, 2, 3, 5, 6, 7, 8, 9],
                              1: [0, 1, 2, 6, 7, 8],
                              2: [0, 1, 2, 3, 5, 6, 7, 8],
                              3: [0, 2, 3, 5, 6, 8],
                              5: [0, 2, 3, 5, 6, 8],
                              6: [0, 1, 2, 3, 5, 6, 7, 8],
                              7: [0, 1, 2, 6, 7, 8],
                              8: [0, 1, 2, 3, 5, 6, 7, 8, 9]}

    for x in range(1, 10):
      for y in range(13, 22):
        offset_canvas.SetPixel(x, y, 255, 255, 255)

    for y, x_vals in arrow_corrections_black.items():
      for x in x_vals:
        offset_canvas.SetPixel(1+x, 13+y, 0, 0, 0)

    for y in range(32):
      offset_canvas.SetPixel(29, y, 255, 255, 255)

    ghost_corrections_black = {0: [0, 1, 2, 3, 4, 9, 10, 11, 12, 13],
                              1: [0, 1, 2, 11, 12, 13],
                              2: [0, 1, 12, 13],
                              3: [0, 4, 5, 10, 11, 13],
                              4: [0, 3, 4, 5, 6, 9, 10, 11, 12, 13],
                              5: [0, 3, 4, 9, 10, 13],
                              6: [3, 4, 9, 10],
                              7: [4, 5, 10, 11],
                              12: [2, 6, 7, 11],
                              13: [1, 2, 3, 6, 7, 10, 11, 12]}

    ghost_corrections_white = {5: [5, 6, 11, 12],
                               6: [5, 6, 11, 12]}


    for x in range(12, 26):
      for y in range(0, 14):
        offset_canvas.SetPixel(x, y, 0, 0, 255)

    for y, x_vals in ghost_corrections_black.items():
      for x in x_vals:
        offset_canvas.SetPixel(12+x, y, 0, 0, 0)

    for y, x_vals in ghost_corrections_white.items():
      for x in x_vals:
        offset_canvas.SetPixel(12+x, y, 255, 255, 255)

    my_text = "PAC-MAN"
    len = graphics.DrawText(offset_canvas, font, 33, 7, graphics.Color(255, 255, 0), my_text)
    # fix the 'N'
    offset_canvas.SetPixel(57, 2, 255, 255, 0)
    offset_canvas.SetPixel(59, 6, 255, 255, 0)


    for x in range(30, 64):
      offset_canvas.SetPixel(x, 8, 255, 255, 255)

    my_text = "EAT DOTS"
    len = graphics.DrawText(offset_canvas, font, 31, 16, textColor, my_text)

    for x in range(32, 62):
      offset_canvas.SetPixel(x, 18, 0, 0, 255)

    for x in range(32, 62):
      offset_canvas.SetPixel(x, 30, 0, 0, 255)

    for y in range(18, 30):
      offset_canvas.SetPixel(32, y, 0, 0, 255)

    for y in range(18, 31):
      offset_canvas.SetPixel(62, y, 0, 0, 255)

    dots = [(37, 28), (42, 20), (55, 27), (60, 21)]

    for x, y in dots:
      offset_canvas.SetPixel(x, y, *PacmanGame.FOOD_COLOR)

    pacman = (45, 26)
    offset_canvas.SetPixel(*pacman, *PacmanGame.PACMAN_COLOR)

    matrix_panel.matrix.SwapOnVSync(offset_canvas)

    walls = dict([((i, 18), True) for i in range(32, 62)] + [((i, 30), True) for i in range(32, 62)] + 
                 [((32, j), True) for j in range(18, 30)] + [((62, j), True) for j in range(18, 31)])

    while True:
      pitch, roll = matrix_panel.get_mpu_pitch_roll()
      x_old, y_old = pacman

      if abs(pitch) > abs(roll):
        x = (x_old + 1) if pitch > 0 else (x_old - 1)
        y = y_old
      else:
        x = x_old
        y = (y_old + 1) if roll > 0 else (y_old - 1)

      if (x, y) not in walls:
        offset_canvas.SetPixel(x, y, *PacmanGame.PACMAN_COLOR)
        offset_canvas.SetPixel(x_old, y_old, 0, 0, 0)
        matrix_panel.matrix.SwapOnVSync(offset_canvas)

        pacman = (x, y)

      time.sleep(0.5)


  def read_board_in(self, filename):
    walls, food, power_pellets, blanks = {}, {}, {}, {}
    pacman = None
    enemies = {}
    with open(filename) as f:
      for y, line in enumerate(f):
        for x, val in enumerate(line):
          if x < 0 or x > PacmanGame.GAME_BOARD_LENGTH or y < 0 or y > PacmanGame.GAME_BOARD_HEIGHT:
            continue
          if val == "\n":
            continue
          if val == "X":
            walls[(x, y)] = True
          elif val == ".":
            food[(x, y)] = True
          elif val == "S":
            power_pellets[(x, y)] = True
          elif val == "_" or val == " ":
            blanks[(x, y)] = True
          elif val == "P":
            pacman = (x, y)
          elif val == "E":
            enemies[(x, y)] = True
          else:
            assert False, f"Character {val} not recognized"
    assert pacman != None, "Pacman has not been initialized"
    return walls, food, power_pellets, blanks, pacman, enemies

  def update_game_state(self, matrix_panel, offset_canvas, pitch, roll, volume_level):
    # Main function that takes input and makes changes to the game state based on inputs
    
    # First update the Pacman position based on the pitch / roll
    self.move_pacman(matrix_panel, offset_canvas, pitch, roll)

    # Then have the Enemy/Ghost AI update their positions
    if self.ghosts_active:
      self.move_ghosts()
      self.ghosts_timesteps_left -= 1
      if self.ghosts_timesteps_left < 0:
        self.ghosts_active = False
    else:
      self.move_enemies(matrix_panel, offset_canvas)

    # Finally check if the "level" has been cleared
    if len(self.food) == 0 and len(self.power_pellets) == 0:
      # TODO maybe load a different board in (involves parsing a new file, setting the walls, food, etc, then init board)
      self.init_board(matrix_panel)


  def init_board(self, matrix_panel, offset_canvas, reset=False):
    # Called when the matrix panel is first booting up the game OR after a death
    if not reset:
      for x, y in self.walls.keys():
        offset_canvas.SetPixel(x, y, *PacmanGame.WALL_COLOR)
    for x, y in self.food.keys():
      offset_canvas.SetPixel(x, y, *PacmanGame.FOOD_COLOR)
    for x, y in self.power_pellets.keys():
      offset_canvas.SetPixel(x, y, *PacmanGame.POWER_PELLETS_COLOR)

    offset_canvas.SetPixel(*self.pacman_init, *PacmanGame.PACMAN_COLOR)

    for (x, y), enemy_color in zip(self.enemies_init.keys(), PacmanGame.ENEMY_COLORS):
      offset_canvas.SetPixel(x, y, *enemy_color)

  def update_board(self):
    # Called after the matrix panel has updated the game state
    # TODO REMOVE THIS FUNCTION

    #for x, y in self.food.keys():
    #  offset_canvas.SetPixel(x, y, *PacmanGame.FOOD_COLOR)

    #for x, y in self.power_pellets.keys():
    #  offset_canvas.SetPixel(x, y, *PacmanGame.POWER_PELLETS_COLOR)

    #offset_canvas.SetPixel(*self.pacman, *PacmanGame.PACMAN_COLOR)

    #for (x, y), enemy_color in zip(self.enemies.keys(), PacmanGame.ENEMY_COLORS):
    #  offset_canvas.SetPixel(x, y, *enemy_color)
    pass

  def move_pacman(self, matrix_panel, offset_canvas, pitch, roll):
    x_old, y_old = self.pacman

    if abs(pitch) > abs(roll):
      x = (x_old + 1) % PacmanGame.GAME_BOARD_LENGTH if pitch > 0 else (x_old - 1) % PacmanGame.GAME_BOARD_LENGTH 
      y = y_old
    else:
      x = x_old
      y = (y_old + 1) % PacmanGame.GAME_BOARD_HEIGHT if roll > 0 else (y_old - 1) % PacmanGame.GAME_BOARD_HEIGHT

    if (x, y) not in self.walls and ((x, y) not in self.enemies or self.ghosts_active):
      offset_canvas.SetPixel(x, y, *PacmanGame.PACMAN_COLOR)
      offset_canvas.SetPixel(x_old, y_old, 0, 0, 0)
      offset_canvas = matrix_panel.matrix.SwapOnVSync(offset_canvas)

      self.pacman = (x, y)
      # Only have to update the score if there was movement
      self.update_score(x, y)
    elif (x, y) in self.enemies and not self.ghosts_active:
      self.lives -= 1
      if self.lives == 0:
        # Game over
        self.display_final_score(matrix_panel)
        self.game_over = True
      else:
        # Reset the board
        self.init_board(matrix_panel, offset_canvas, reset=True)
    elif (x, y) in self.enemies and self.ghosts_active:
      # put ghost in jail
      # TODO
      pass

  def update_score(self, x, y):
    # Only check if the movement was into a food or power pellet square
    # Also remove (x, y) from the food or power pellets dict
    if (x, y) in self.food:
      self.score += 10
      self.food.pop((x, y))
    elif (x, y) in self.power_pellets:
      self.score += 50
      self.power_pellets.pop((x, y))
    # Ghost could be on a square with food / power pellet in which case pacman would get points for both
    if (x, y) in self.enemies and self.ghosts_active:
      self.score += 200

  def display_final_score(self, matrix_panel):
    # Just use draw text to display final score
    #run_text = RunText(f"Game over! Score: {self.score}")
    #run_text.process()
    pass

  def move_enemies(self, matrix_panel, offset_canvas):
    for (x_old, y_old), enemy_color in zip(self.enemies.keys(), PacmanGame.ENEMY_COLORS):
      # First check if the enemy is in jail and decrease timesteps for it; move out of jail if needed

      # First figure out the next best position for this enemy to move
      # Two modes: follow player, ambush player 
      # Make sure ghosts don't collide with walls, each other; collision with pacman?
      x, y = x_old, y_old # TODO

      #offset_canvas.SetPixel(x, y, *enemy_color)


  def move_ghosts(self):
    pass
  
if __name__ == "__main__":  
  mpu_queue = Queue()

  i2c = board.I2C()  # uses board.SCL and board.SDA
  mpu = adafruit_mpu6050.MPU6050(i2c)
  mpu_thread = threading.Thread(target=read_pitch_roll, args=(mpu, mpu_queue,))
  mpu_thread.start()

  matrix_panel = MatrixPanel(mpu_queue)
  matrix_panel_thread = threading.Thread(target=matrix_panel.process, args=())
  matrix_panel_thread.start()

  #if (not matrix_panel.process()):
  #  matrix_panel.print_help()