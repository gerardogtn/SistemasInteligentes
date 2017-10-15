from positionable import Positionable
from drawable import Drawable
import random
import math

class SimpleExplorer(Positionable, Drawable):
  SIZE = 7
  MAX_SPEED = 1.3
  SENSOR_RANGE = 10
  COLOR = 'blue'
  HAS_SAMPLE_COLOR = 'yellow'
  SENSOR_COLOR = 'yellow'
  AVOID_TIME = 10

  def __init__(self, world, x, y, ship):
    self.world = world
    self.sample = False
    self.ship = ship
    self.dx = -1
    self.dy = -1
    self.avoidingTime = 0
    super().__init__(x, y, self.SIZE)

  def draw(self, canvas):
    """ Draws the explorer and the sensor range."""
    halfSize = self.SIZE / 2
    canvas.create_oval(self.x - (halfSize),
                       self.y - (halfSize),
                       self.x + (halfSize),
                       self.y + (halfSize),
                       fill=self.HAS_SAMPLE_COLOR if self.sample else self.COLOR)
    canvas.create_oval(self.x - (halfSize + self.SENSOR_RANGE),
                       self.y - (halfSize + self.SENSOR_RANGE),
                       self.x + (halfSize + self.SENSOR_RANGE),
                       self.y + (halfSize + self.SENSOR_RANGE),
                       outline=self.SENSOR_COLOR)


  def tick(self):
    """ Follows the rules established in the agent's model """
    if (not self.cantMove() and self.avoidingObstacle()):
      self.continueAvoidingObstacle()
    elif self.cantMove():
      self.avoidObstacle()
    elif self.hasSample() and self.isInShip():
      self.releaseSample()
    elif self.hasSample():
      self.goToShip()
    elif self.foundSample():
      self.pickSample()
    else:
      self.explore()

  def avoidingObstacle(self): 
    return self.avoidingTime > 0

  def continueAvoidingObstacle(self):
    self.avoidingTime = self.avoidingTime - 1
    self.move()

  def cantMove(self):
    """ Returns true if the explorer cant move """
    nextPos = Positionable(self.x + self.dx, self.y + self.dy, self.SIZE)
    for obstacle in self.world.obstacles:
      if obstacle.overlaps(nextPos):
        return True
    return nextPos.x < 0 or nextPos.x > self.world.width or nextPos.y < 0 or nextPos.y > self.world.height

  def avoidObstacle(self):
    """ Avoids an obstacle by simply changing direction """
    self.avoidingTime = self.AVOID_TIME
    while self.cantMove():
      self.getRandomDirection()
    self.move()

  def hasSample(self):
    """ Returns true if the explorer has a sample """
    return self.sample

  def isInShip(self):
    """ Returns true if the explorer overlaps the ship """
    return self.ship.overlaps(self)

  def releaseSample(self):
    """ Sets the explorer as not having a sample and lets the ship
    know that a sample has been delivered.
    """
    self.sample = False
    self.world.collectSample()

  def goToShip(self):
    """ Sets the moving direction to the shortest line to the ship 
    at maximum speed and moves. 
    """
    deltaX = self.ship.x - self.x
    deltaY = self.ship.y - self.y

    self.dy = deltaY * self.MAX_SPEED / math.sqrt(deltaX ** 2 + deltaY ** 2)
    self.dx = self.dy * deltaX / deltaY

    self.move()

  def foundSample(self):
    """ Returns true if a sample is found """
    radar = Positionable(self.x, self.y, (self.SIZE / 2) + 2 * self.SENSOR_RANGE)
    for s in self.world.samples: 
      if radar.overlaps(s):
        return True
    return False

  def pickSample(self):
    """ Picks up a sample. That is, it lets the world know that a 
    sample was picked and sets the explorer as having a sample
    """
    radar = Positionable(self.x, self.y, self.SIZE + 2 * self.SENSOR_RANGE)
    for s in self.world.samples: 
      if s.overlaps(radar):
        self.sample = True
        self.world.pickSample(s)
        return

  def explore(self):
    """ Sets the explorer direction to random """
    self.move()

  def getRandomDirection(self):
    """ Sets the explorer direction to a random one."""
    deltaX = random.uniform(-self.MAX_SPEED, self.MAX_SPEED)
    deltaY = random.uniform(-self.MAX_SPEED, self.MAX_SPEED)

    self.dy = deltaY * self.MAX_SPEED / math.sqrt(deltaX ** 2 + deltaY ** 2)
    self.dx = self.dy * deltaX / deltaY

  def move(self):
    """ Moves the explorer in the direction specified by dx and dy"""
    self.x = self.x + self.dx
    self.y = self.y + self.dy


  def random(num, width, height, world, ship):
    explorers = []
    while len(explorers) < num:
      x = random.randint(0, width)
      y = random.randint(0, height)
      explorer = SimpleExplorer(world, x, y, ship)
      if (world.fits(explorer)):
        explorers.append(explorer)

    return explorers