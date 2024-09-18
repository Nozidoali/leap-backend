from setuptools import setup, find_packages

setup(
    name="backend",
    version="0.1.0",
    author="Hanyu Wang",
    description="LEAP backend.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(include=["backend", "backend.*"]),
)
