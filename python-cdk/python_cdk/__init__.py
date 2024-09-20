import os
import sys

# Get the current directory of the __init__.py file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the current directory to the Python path
sys.path.append(current_dir)

# Import the modules from the current directory
from Configuration import Configuration