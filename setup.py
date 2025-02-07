from setuptools import setup, find_packages

setup(
    name="configs_cli",
    version="0.1.0",
    description="A CLI tool to install dependencies and set up your dotfiles",
    author="Your Name",
    packages=find_packages(),
    scripts=['configs_cli/bin/configs-cli'],
    python_requires=">=3.6",
)

