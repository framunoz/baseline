import pathlib

from pkg_resources import parse_requirements
from setuptools import find_packages, setup

# List of requirements
with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement) for requirement in parse_requirements(requirements_txt)
    ]

setup(
    name="despliegue",
    packages=find_packages(),
    version="0.1.0",
    description="Libreria para la baseline de despliegue",
    author="F. Muñoz",
    author_email="fmunoz@ug.uchile.cl",
    license="MIT",
    install_requires=install_requires,
)
