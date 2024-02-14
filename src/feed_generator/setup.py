from setuptools import find_packages, setup

setup(
    name='feed-generator',
    version='1.0.0',
    packages=find_packages(),
    package_data={"": ["*.yaml"]},
    url='',
    license='',
    author='Talentify',
    author_email='',
    description='',
    entry_points={
        "console_scripts": [
            "run=feed_generator.main:main",
        ],
    },
)
