from drawable import Drawable
from positionable import Positionable
import random

class Obstacle(Drawable, Positionable):
  SIZE = 20
  COLOR = 'gray'

  def __init__(self, x, y):
    super().__init__(x, y, self.SIZE)

  def draw(self, canvas):
    canvas.create_oval(self.x - self.SIZE / 2,
                       self.y - self.SIZE / 2, 
                       self.x + self.SIZE / 2, 
                       self.y + self.SIZE / 2, 
                       fill= self.COLOR)

  @staticmethod
  def random(num, width, height, world):
    obstacles = []
    while len(obstacles) < num:
      x = random.randint(0, width)
      y = random.randint(0, height)
      obstacle = Obstacle(x, y)
      if (world.fits(obstacle)):
        obstacles.append(obstacle)

    return obstacles