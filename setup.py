from setuptools import find_packages, setup
from app.modules.setup.loader import load_instruments
import os
import fnmatch

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


def find_reference_datafile(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def setup_reference_data(dataset, filename):
    file_matches = find_reference_datafile(filename, '.')
    if file_matches:
        load_instruments(dataset, file_matches[0])
    else:
        raise ValueError('No Appropriate File Matching with {}'.format(filename))


setup_reference_data(dataset='CHRIS', filename ='CHRIS_metadata.csv')
