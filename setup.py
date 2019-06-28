from setuptools import find_packages, setup
from app.modules.setup.loader import load_instruments
from pathlib import Path, PureWindowsPath

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)

filename = PureWindowsPath('./data/CHRIS_metadata.csv')
correct_path = Path(filename)
load_instruments('CHRIS', correct_path)
