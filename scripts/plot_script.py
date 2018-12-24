# -*- coding: utf-8 -*

import re
import sys

script_file_folder = (re.match(".*\\\\", sys.argv[0])).group(0)

from modules.PlotScript import *

plot_script = PlotScript()
plot_script.main(sys.argv)
