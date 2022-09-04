from setuptools import setup

setup(
    name="Gridy",
    version="1.0",
    py_modules=["main"],
    install_requires=["Click"],
    entry_points='''
        [console_scripts]
        gridy=main:cli
    ''',
)
