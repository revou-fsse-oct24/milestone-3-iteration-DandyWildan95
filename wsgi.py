import os
import sys

# Add the project root to Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

try:
    from src.app import create_app
    app = create_app()
except Exception as e:
    print(f"Error importing app: {e}")
    raise

if __name__ == '__main__':
    app.run()
