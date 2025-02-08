from setuptools import setup, find_packages

setup(
    name="configs_cli",
    version="0.1.0",
    description="A CLI tool to install dependencies and set up your dotfiles",
    author="Your Name",
    packages=find_packages(),
    scripts=['configs_cli/bin/configs-cli'],
    python_requires=">=3.6",
    install_requires=[
        'argparse',
        'setuptools>=64',
        'wheel',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System :: Installation/Setup',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

