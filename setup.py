import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fsdemo-dyslab",
    version="0.1.5",
    author="DYSLAB",
    author_email="vincent_to@qq.com",
    description="A demo project about Python/Flask website building",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dyslab/flask-site-demo.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
