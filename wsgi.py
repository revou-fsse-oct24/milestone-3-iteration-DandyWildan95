import os
import sys

# Print initial diagnostic information
print("Current Python executable:", sys.executable)
print("Current working directory:", os.getcwd())

# Determine the absolute path of the project root
project_root = os.path.abspath(os.path.dirname(__file__))
print("Project root:", project_root)

# Add project root and src to Python path
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

# Additional diagnostic information
print("Python path:", sys.path)
print("Contents of current directory:", os.listdir('.'))
print("Contents of project root:", os.listdir(project_root))

try:
    # Try importing with different methods
    import src
    from src.app import create_app
    app = create_app()
except ImportError as e:
    print(f"Import error: {e}")
    
    # More aggressive diagnostic information
    print("Attempting to list src contents:")
    try:
        print(os.listdir('src'))
    except Exception as list_error:
        print(f"Error listing src: {list_error}")
    
    # Print all Python files in the project
    print("Python files in project:")
    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file.endswith('.py'):
                print(os.path.join(root, file))
    
    raise

if __name__ == '__main__':
    app.run()
