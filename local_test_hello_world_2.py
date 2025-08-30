import json
import sys
import os

# Agregar el layer al PYTHONPATH para testing local
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'shared'))

from hello_world_2 import app

def main():
    with open("events/event.json") as f:
        event = json.load(f)
    context = None
    result = app.lambda_handler(event, context)
    print(result)

if __name__ == "__main__":
    main()
