from drawable import Drawable

class World(Drawable):
  BACKGROUND = "#a75a35"

  def __init__(self, width, height, existingSamples, samples=[], obstacles=[], explorers=[]):
    """ Creates a new World of width x height with rocks. 

    Keyword arguments: 
    width -- width of the screen in pixels.
    height -- height of the screen in pixels.
    samples -- a list of samples (defaults to empty).
    obstacles -- a list of obstacles (defaults to empty).
    explorers -- a list of explorers (dfaults to empty).
    """
    self.width = width
    self.height = height
    self.base = None
    self.obstacles = obstacles
    self.explorers = explorers
    self.samples = samples
    self.collectedSamples = 0
    self.onFinish = lambda x: None
    self.existingSamples = existingSamples

  def pickSample(self, sample): 
    """ Called when a Explorer picks up a sample """
    self.samples.remove(sample)

  def collectSample(self):
    """ Call this method if a rock is collected. If there are no more rocks self.onFinish()
    is called. 

    Keyword arguments: 
    rock -- the rock to collect.
    """
    self.collectedSamples = self.collectedSamples + 1

  def tick(self):
    """ Tells all explorers and simpleExplorers that a tick event occurred. """
    for e in self.explorers:
        e.tick()

  def draw(self, canvas): 
    """ Draws all elements"""
    canvas.configure(background=self.BACKGROUND)
    self.base.draw(canvas)
    for e in self.explorers + self.obstacles + self.samples:
        e.draw(canvas)

  def fits(self, positionable):
    """ Returns true if the positionable can be fitted into the world

    Keyword arguments:
    positionable -- the positionable we're checking if fits
    """
    for e in self.samples + self.obstacles + self.explorers: 
      if e.overlaps(positionable):
        return False
    return True

