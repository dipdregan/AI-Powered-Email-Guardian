import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.0"

REPO_NAME="Ham_Spam_Classifier(ETE)"
AUTHOR_NAME="dipdregan"
AUTHOR_Email="dipendrapratap155@gmail.com"

setuptools.setup(
    version=__version__,
    author=AUTHOR_NAME,
    author_email=AUTHOR_Email,
    description="this is ham spam prediction project",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_NAME}/{REPO_NAME}",
    
    project_urls={
                  
    "Bug Tracker": f"https://github.com/{AUTHOR_NAME}/{REPO_NAME}/issues",  
                  
                 },
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
    
)