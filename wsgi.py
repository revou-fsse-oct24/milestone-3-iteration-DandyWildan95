import os
import sys

# Ensure the project root is in the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Add explicit path for src
sys.path.insert(0, os.path.join(project_root, 'src'))

# Diagnostic print statements
print("Current working directory:", os.getcwd())
print("Project root:", project_root)
print("Python path:", sys.path)
print("Contents of current directory:", os.listdir('.'))
print("Contents of src directory:", os.listdir('src') if os.path.exists('src') else "src directory not found")

try:
    from src.app import create_app
    app = create_app()
except ImportError as e:
    print(f"Import error: {e}")
    raise

if __name__ == '__main__':
    app.run()
