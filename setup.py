from setuptools import setup, find_packages

setup(
    name="configs_cli",
    version="0.2.0",
    description="CLI tool for setting up a headless development environment",
    author="Your Name",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'configs-cli=configs_cli.main:main',
        ],
    },
    python_requires=">=3.9",
    install_requires=[
        'rich>=13.0.0',
        'setuptools>=64',
        'wheel',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System :: Installation/Setup',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)

