from optparse import OptionParser
from base import Base
from simple_explorer import SimpleExplorer
from obstacle import Obstacle
from sample import Sample
from world import World
from gui import Gui

def main():
  usage = "usage: %prog [options] filename"
  parser = OptionParser(usage=usage)
  parser.add_option("-w", "--width", dest="width", type="int", default=800,
    help="Set the width of the window, defaults to 800")
  parser.add_option("--height", dest="height", type="int",
    default=600, help="Set the height of the window, defaults to 600.")
  parser.add_option("-e", "--explorers", dest="explorers", type="int",
    default=5, help="The number of explorers, defaults to 5")
  parser.add_option("-s", "--samples", dest="samples", type="int",
    default=10, help="The number of samples to appear, defaults to 10")
  parser.add_option("-o", "--obstacles", dest="obstacles", type="int", 
    default=7, help="The number of obstacles, defaults to 7.")
  options, args = parser.parse_args()
 
  world = World(options.width, options.height, options.samples)
  base = Base(options.width / 2, options.height / 2)
  world.base = base
  world.explorers = SimpleExplorer.random(options.explorers, options.width, options.height, world, base)
  world.samples = Sample.random(options.samples, options.width, options.height, world)
  world.obstacles = Obstacle.random(options.obstacles, options.width, options.height, world)

  gui = Gui(options.width, options.height, world)
  gui.start()

if __name__ == '__main__':
  main()