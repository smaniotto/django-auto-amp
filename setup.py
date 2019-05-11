import os
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md")).read()

setup(
    name="django-auto-amp",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    description="Generate automatic AMP from your Django templates",
    long_description=README,
    author="Bernardo Smaniotto",
    author_email="be.smaniotto@gmail.com",
    url="https://github.com/smaniotto/django-auto-amp/",
    license="MIT",
    install_requires=["Django>=1.11,<=2.2", "beautifulsoup>=4,<=5"],
)
