from setuptools import find_packages, setup

setup(
    name="feed-downloader",
    version="1.0.0",
    packages=find_packages(),
    package_data={"": ["*.yaml", "*.raw", ""]},
)
