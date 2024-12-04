import os
import sys
import subprocess
import platform

def create_venv(venv_name):
    """Create a virtual environment."""
    if platform.system() == "Windows":
        subprocess.check_call([sys.executable, "-m", "venv", venv_name])
    else:  # For macOS and Linux
        subprocess.check_call([sys.executable, "-m", "venv", venv_name])

def install_requirements(venv_name):
    """Install packages from requirements.txt."""
    pip_executable = os.path.join(venv_name, 'Scripts', 'pip') if platform.system() == "Windows" else os.path.join(venv_name, 'bin', 'pip')
    
    # Check if requirements.txt exists
    if os.path.exists('requirements.txt'):
        subprocess.check_call([pip_executable, "install", "-r", "requirements.txt"])
    else:
        print("requirements.txt not found.")

def main():
    venv_name = "myenv"  # Name of the virtual environment

    # Create the virtual environment
    create_venv(venv_name)
    
    # Install requirements
    install_requirements(venv_name)

if __name__ == "__main__":
    main()