from setuptools import setup, find_packages

setup(
    name='notion_api_sdk',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "numpy=1.25.2",
        "pandas=1.5.3"
    ],
    author="Andy Lee",
    author_email="anddy0622@gmail.com",
    description="Please see https://github.com/AndyLeeProjects/Notion_API",
)
