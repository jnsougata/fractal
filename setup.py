from setuptools import setup

with open("README.md") as f:
    readme = f.read()


setup(
    name="fractal",
    version="0.0.1",
    description="A lightweight, simple, and fast SQLite wrapper for Python.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/jnsougata/fractal",
    author="Sougata Jana",
    author_email="jnsougata@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    packages=["fractal"],
    keywords="sqlite, wrapper, database, lightweight, sqlite3, KV, storage",
    python_requires=">=3.8.0",
)
