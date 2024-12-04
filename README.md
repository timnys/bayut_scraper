# Bayut Scraper

The **Bayut Scraper** is a Python tool designed to scrape property listings from the Bayut website. It automatically sets up a Python virtual environment and installs required packages for smooth operation.

## Features

- Scrapes property listings, including details like price, location, and amenities.
- Saves the scraped data into a CSV file for easy access and analysis.

## Table of Contents

- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Other Option](#other-option)
- [Output](#output)
- [License](#license)

## Requirements

- Python 3.x
- pip (Python package installer)

## Setup Instructions (For virtual env)

To set up the environment, choose one of the following scripts based on your operating system:

### For Windows

1. Run the `run_script.bat`:
   ```bash
   run_script.bat
   ```

This script will:

- Create a virtual environment named `myenv`
- Activate the virtual environment
- Install packages specified in `requirements.txt`
- Run the `myscript.py`
- Deactivate the virtual environment

### For Linux/Mac

1. Run the `run_script.sh`:
   ```bash
   ./run_script.sh
   ```

The `run_script.sh` performs similar steps as the Windows script, creating and setting up the virtual environment.

### Script Contents

**run_script.bat**

```batch
@echo off
call myenv\Scripts\activate
python myscript.py
python main.py
deactivate
```

**myscript.py**

```python
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
```

## Other option

You can install the python packages globally and run `main.py` directly without using virtual env

```bash
pip install -r requirements.txt
python main.py
```

## Output

The results of the scraping will be saved to an `output.csv` file. The CSV will include the following fields:

- `url`
- `currency`
- `price`
- `location`
- `bed`
- `bath`
- `sqft`
- `description`
- `car_parking`
- `type`
- `purpose`
- `trucheck_date`
- `reference_no`
- `average_rent`
- `completion_status`
- `added_on`
- `fitness`
- `developer`
- `usage`
- `ownership`
- `swimming_pool`
- `floors`
- `total_floors`
- `furnishing`
- `elevators`
- `completion_year`
- `security_staff`
- `central_heating`
- `centrally_air-conditioned`
- `balcony_or_terrace`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
