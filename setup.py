from setuptools import setup, find_packages

setup(
    name="wifidaemon",
    version="2.0.0-DEMON",
    author="Anonymous-beta",
    author_email="anonym09g@gmail.com",
    description="Advanced WiFi Pentesting Framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/anonymous-beta/Wifidaemon",
    packages=find_packages(),
    install_requires=[
        "scapy>=2.5.0",
        "rich>=13.0.0",
        "psutil>=5.9.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "wifidaemon=daemon.main:main",
        ],
    },
)
