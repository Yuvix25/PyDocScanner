import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyDocScanner",
    #install_requires=['numpy', 'skimage', 'pytesseract', 'imutils', 'pillow'],
    version="0.0.1",
    author="Yuval Rosen",
    author_email="yuv.rosen@gmail.com",
    description="Python document scanner.",
    license="GNU",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Yuvix25/PyDocScanner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)