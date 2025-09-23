"""
Please refer to the documentation provided in the README.md,
which can be found at httpie-edgegrid's PyPI URL: https://pypi.org/project/httpie-edgegrid/
"""

from setuptools import setup

def get_readme():
    """Returns the content of README.md"""
    with open('README.md') as readme:
        return readme.read()

setup(
    name='httpie-edgegrid',
    description='Edgegrid plugin for HTTPie.',
    python_requires=">=3.9",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    version='2.2.3',
    license='Apache 2.0',
    url='https://github.com/akamai/httpie-edgegrid',
    download_url='https://github.com/akamai/httpie-edgegrid',
    py_modules=['httpie_edgegrid'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_oauth1 = httpie_edgegrid:EdgeGridPlugin'
        ]
    },
    install_requires=[
        'httpie >= 3.0.0',
        'edgegrid-python >= 2.0.2',
    ],
    extras_require={
        'dev': [
            'pylint>=2.15.0',
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0'
        ],
    },
)
