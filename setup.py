"""
Setup script para Alexandria: Biblioteca de Interoperabilidade e Programação Comparada
"""

from setuptools import setup, find_packages
from pathlib import Path

# Lê o README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Lê requirements
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="alexandria-lang",
    version="0.1.0",
    author="Alexandria Team",
    author_email="alexandria@programacao-comparada.org",
    description="Biblioteca de Interoperabilidade e Programação Comparada",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/alexandria",
    project_urls={
        "Bug Tracker": "https://github.com/seu-usuario/alexandria/issues",
        "Documentation": "https://alexandria-lang.readthedocs.io/",
        "Source Code": "https://github.com/seu-usuario/alexandria",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Compilers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Education",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "visualization": [
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
            "plotly>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "alexandria=alexandria.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "alexandria": [
            "data/*.json",
            "docs/*.md",
        ],
    },
    keywords=[
        "programming languages",
        "comparative analysis",
        "interoperability",
        "code translation",
        "type mapping",
        "language bridges",
        "programming education",
        "research",
    ],
) 