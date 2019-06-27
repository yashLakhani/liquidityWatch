from setuptools import find_packages, setup
from app.modules.setup.loader import load_instruments
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

load_instruments('CHRIS', '/Users/yashl/PycharmProjects/liquidityWatch/app/data/CHRIS_metadata.csv')
