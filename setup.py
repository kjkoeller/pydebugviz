from setuptools import setup, find_packages

setup(
    name="pydebugviz",
    version="1.0.0",
    description="Time-travel debugger and visualization toolkit for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Kyle Koeller",
    # author_email="you@example.com",
    url="https://github.com/kjkoeller/pydebugviz",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.2",
        "ipywidgets>=8.1",
        "networkx>=3.2",
        "matplotlib>=3.8"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
    zip_safe=False,
)
