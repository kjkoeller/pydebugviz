from setuptools import setup, find_packages

setup(
    name="pydebugviz",
    version="1.5.0",
    description="Robust Python debugger with trace validation and visual tools",
    packages=find_packages(),
    install_requires=["ipywidgets", "matplotlib", "pandas", "networkx"],
    entry_points={
        "console_scripts": [
            "pydebugviz=pydebugviz.cli:main"
        ]
    },
    python_requires=">=3.7"
)
