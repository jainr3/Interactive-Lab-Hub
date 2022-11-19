#!/usr/bin/env python
from samplebase import SampleBase
import adafruit_mpu6050, board, math, time, threading
from queue import Queue

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
  def __init__(self, mpu_queue, game, *args, **kwargs):
    self.mpu_queue = mpu_queue
    self.game = game
    super(MatrixPanel, self).__init__(*args, **kwargs)

  def run(self):
    offset_canvas = self.matrix.CreateFrameCanvas()

    self.game.init_board(offset_canvas)

    while True:
      # Get the inputs synchronously
      pitch, roll = self.get_mpu_pitch_roll()
      volume_level = self.get_volume_level()

      # Update the game state and screen, every game should have a main function
      self.game.update_game_state(self, offset_canvas, pitch, roll, volume_level)
        
      #time.sleep(0.5)

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

  GAME_BOARD_LENGTH = 62 # leave 2 pixels on right side for score / lives
  GAME_BOARD_HEIGHT = 32

  def __init__(self, file):
    self.walls, self.food, self.power_pellets, self.blanks, self.pacman, self.enemies = self.read_board_in(file)
    self.score = 0
    self.lives = 3

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

    # Then have the Ghost AI update their positions


  def init_board(self, offset_canvas):
    # Called when the matrix panel is first booting up the game
    for x, y in self.walls.keys():
      offset_canvas.SetPixel(x, y, *PacmanGame.WALL_COLOR)
    for x, y in self.food.keys():
      offset_canvas.SetPixel(x, y, *PacmanGame.FOOD_COLOR)
    for x, y in self.power_pellets.keys():
      offset_canvas.SetPixel(x, y, *PacmanGame.POWER_PELLETS_COLOR)

    offset_canvas.SetPixel(*self.pacman, *PacmanGame.PACMAN_COLOR)

    for (x, y), enemy_color in zip(self.enemies.keys(), PacmanGame.ENEMY_COLORS):
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

  def update_pacman_color(self):
    x, y = self.pacman


  def move_pacman(self, matrix_panel, offset_canvas, pitch, roll):
    x_old, y_old = self.pacman

    if abs(pitch) > abs(roll):
      x = (x_old + 1) % PacmanGame.GAME_BOARD_LENGTH if pitch > 0 else (x_old - 1) % PacmanGame.GAME_BOARD_LENGTH 
      y = y_old
    else:
      x = x_old
      y = (y_old + 1) % PacmanGame.GAME_BOARD_HEIGHT if roll > 0 else (y_old - 1) % PacmanGame.GAME_BOARD_HEIGHT


    if (x, y) not in self.walls and (x, y) not in self.enemies:
      offset_canvas.SetPixel(x, y, *PacmanGame.PACMAN_COLOR)
      offset_canvas.SetPixel(x_old, y_old, 0, 0, 0)
      offset_canvas = matrix_panel.matrix.SwapOnVSync(offset_canvas)

      self.pacman = (x, y)


  def move_enemies(self):
    pass
  
  def move_ghosts(self):
    pass
  
if __name__ == "__main__":  
  file = 'pacman_board_2.txt'
  pacman_game = PacmanGame(file)

  mpu_queue = Queue()

  i2c = board.I2C()  # uses board.SCL and board.SDA
  mpu = adafruit_mpu6050.MPU6050(i2c)
  mpu_thread = threading.Thread(target=read_pitch_roll, args=(mpu, mpu_queue,))
  mpu_thread.start()

  matrix_panel = MatrixPanel(mpu_queue, pacman_game)
  matrix_panel_thread = threading.Thread(target=matrix_panel.process, args=())
  matrix_panel_thread.start()

  #if (not matrix_panel.process()):
  #  matrix_panel.print_help()