# -*- coding: utf-8 -*

import re
import sys

script_file_folder = (re.match(".*\\\\", sys.argv[0])).group(0)

from modules.Plotter import *

plotter = Plotter()
plotter.main(sys.argv)
