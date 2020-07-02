import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ledsign-tishka25", # Replace with your own username
    version="0.0.1",
    author="Teodor Stanishev",
    author_email="teodorstanishev@gmail.com",
    description="A small package for controlling Chainzone LED Sign using Ethernet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tishka25/LEDSign.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)