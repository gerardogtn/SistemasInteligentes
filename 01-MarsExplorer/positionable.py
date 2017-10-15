
class Positionable(object):

  def __init__(self, x, y, size):
    self.x = x
    self.y = y
    self.size = size

  def overlaps(self, positionable):
    """ Checks if another positionable would occupy 
    the same position as another positionable. 

    Keyword arguments:
    positionable -- A positionable

    Returns:
    True if the positionables overlap, False otherwise.
    """
    x1 = self.x - self.size / 2
    x2 = self.x + self.size / 2
    y1 = self.y - self.size / 2
    y2 = self.y + self.size / 2

    x3 = positionable.x - positionable.size / 2
    x4 = positionable.x + positionable.size / 2
    y3 = positionable.y - positionable.size / 2
    y4 = positionable.y + positionable.size / 2

    return self._fitsX(x1, x2, x3, x4) and self._fitsY(y1, y2, y3, y4)

  def _fitsX(self, x1, x2, x3, x4):
    return (x3 > x1 and x3 < x2) or (x3 < x1 and x4 > x1)

  def _fitsY(self, y1, y2, y3, y4):
    return (y3 > y1 and y3 < y2) or (y3 < y1 and y4 > y1)
