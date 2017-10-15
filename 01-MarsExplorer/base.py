from drawable import Drawable
from positionable import Positionable

class Base(Drawable, Positionable):
  SIZE = 40
  COLOR = "blue"

  def __init__(self, x, y):
    super(Drawable, self).__init__(x, y, self.SIZE)

  def draw(self, canvas):
    canvas.create_rectangle(self.x - self.size / 2, 
                            self.y - self.size / 2,
                            self.x + self.size / 2,
                            self.y + self.size / 2, 
                            fill=self.COLOR)