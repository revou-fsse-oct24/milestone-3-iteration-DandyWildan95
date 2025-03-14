import os
import sys
import traceback
import glob

# Determine the absolute path of the project root
project_root = os.path.abspath(os.path.dirname(__file__))

# Add project root and src to Python path
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

# Diagnostic print statements
print("Current working directory:", os.getcwd())
print("Project root:", project_root)
print("Python path:", sys.path)

# Function to print directory contents
def print_directory_contents(directory):
    print(f"Contents of {directory}:")
    try:
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            item_type = "directory" if os.path.isdir(full_path) else "file"
            print(f"- {item} ({item_type})")
    except Exception as e:
        print(f"Error listing directory {directory}: {e}")

# Print contents of project root and src directory
print_directory_contents(project_root)
print_directory_contents(os.path.join(project_root, 'src'))

# Print all Python files in the project
print("\nPython files in project:")
for py_file in glob.glob(os.path.join(project_root, '**', '*.py'), recursive=True):
    print(py_file)

try:
    # Attempt to import with maximum diagnostics
    from src.app import create_app
    app = create_app()
except ImportError as e:
    print(f"Import error: {e}")
    print("Traceback:")
    traceback.print_exc()
    raise

if __name__ == '__main__':
    app.run()
