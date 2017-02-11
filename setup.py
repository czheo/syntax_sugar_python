from setuptools import setup, find_packages

setup(
    name="syntax_sugar",
    version="0.2.2",
    url='https://github.com/czheo/syntax_sugar_python',
    description="add syntactic sugar to Python",
    author="czheo",
    license="MIT",
    keywords="syntax, functional",
    packages=find_packages(),
    install_requires=[
        'multiprocess',
        'eventlet',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
