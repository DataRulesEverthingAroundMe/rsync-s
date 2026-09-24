from setuptools import setup, find_packages

setup(
    name="rsync-s",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    entry_points={
        "console_scripts": [
            "rsync-s=rsync_s.main:main",
        ],
    },
)
