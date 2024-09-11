from setuptools import setup, find_packages

setup(
    name='konnsearch',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        "confluent-kafka==2.5.3",
        "opensearch-py==2.7.1",
        "pytest==8.3.2"
    ],
    entry_points={
        'console_scripts': [
            'konnsearch = src.konnsearch.cli:cli',
        ],
    },
)
