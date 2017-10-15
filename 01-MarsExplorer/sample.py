from drawable import Drawable
from positionable import Positionable
import random

class Sample(Drawable, Positionable):
  SIZE = 10
  COLOR = 'green'

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
    samples = []
    while len(samples) < num:
      x = random.randint(0, width)
      y = random.randint(0, height)
      sample = Sample(x, y)
      if (world.fits(sample)):
        samples.append(sample)

    return samples