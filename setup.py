from setuptools import setup, find_packages

setup(
    name='wikipedians',
    version='0.0.1',
    url='https://github.com/he7d3r/wikipedians.git',
    author='Helder Geovane Gomes de Lima',
    author_email='he7d3r@gmail.com',
    description='Explore patterns in wikipedians\' edits',
    packages=find_packages(),
    install_requires=['pandas', 'mwxml'],
)
