import os
import sys

# Add the project root to Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Print diagnostic information
print("Current working directory:", os.getcwd())
print("Project root:", project_root)
print("Python path:", sys.path)

try:
    from src.app import create_app
    app = create_app()
except ImportError as e:
    print(f"Import error: {e}")
    # List contents of current directory for debugging
    import glob
    print("Contents of current directory:", glob.glob('*'))
    print("Contents of src directory:", glob.glob('src/*'))
    raise

if __name__ == '__main__':
    app.run()
