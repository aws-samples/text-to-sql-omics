import os
import sys

# Get the current directory of the __init__.py file
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the current and top directory to the Python path
sys.path.append(current_dir)
sys.path.append(parent_dir)

# Import the modules from the current directory
from lambdas import LambdaConstruct
from api_gateway import APIGatewayConstruct
