from setuptools import setup,find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="KnowFlow_AI_RAG",
    version="0.0.1",
    author="Yasiru lakruwan",
    packages=find_packages(),
    install_requires = requirements
)

# This is the setup file.....