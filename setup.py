"""
GuruDev® — Linguagem Ontológica de Programação
Setup script
"""

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
readme = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="gurudev-core",
    version="0.1.0-alpha",
    author="Guilherme Gonçalves Machado",
    author_email="guilhermemachado.ceo@hubstry.dev",
    description="GuruDev — Linguagem Ontologica de Programacao por Hubstry-DeepTech",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Hubstry-DeepTech/gurudev-core",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "ply>=3.11",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gurudev=src.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Interpreters",
    ],
    keywords=[
        "programming language",
        "ontological",
        "gurudev",
        "hubstry",
        "interpreter",
        "lexer",
        "parser",
    ],
)
