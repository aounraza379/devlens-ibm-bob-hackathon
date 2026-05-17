"""
Setup script for DevLens
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="devlens",
    version="1.0.0",
    author="DevLens Team",
    description="Repository Intelligence & Team Health Dashboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/devlens",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.28.0",
        "groq>=0.4.0",
        "python-dotenv>=1.0.0",
        "textblob>=0.17.0",
        "nltk>=3.8.0",
        "pandas>=2.0.0",
        "plotly>=5.0.0",
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "devlens=app:main",
        ],
    },
)

# Made with Bob
