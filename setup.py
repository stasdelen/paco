import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "paco-pkg-salih",
    version = "0.0.1",
    author = "Salih Tasdelen",
    author_email = "salih.tasdelen@hotmail.com",
    description = "Parser Combinators for Python",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/SalihTasdelen/paco",
    project_urls = {
        "Bug Tracker" : "https://github.com/SalihTasdelen/paco/issues"
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.7"
)