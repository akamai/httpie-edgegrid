"""
Please refer to the documentation provided in the README.md,
which can be found at httpie-edgegrid's PyPI URL: https://pypi.org/project/httpie-edgegrid/
"""

from setuptools import setup

def get_readme() -> str:
    """Returns the content of README.md"""
    with open('README.md') as readme:
        content = readme.read()

    return content.strip()

setup(
    name='httpie-edgegrid',
    description='Edgegrid plugin for HTTPie.',
    python_requires=">=3.7",
    long_description=get_readme(),
    version='2.1.1',
    author='Developer Experience Akamai',
    author_email='devrel@akamai.com',
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
        'httpie == 3.2.1',
        'edgegrid-python == 1.3.1',
        'pyOpenSSL == 22.0.0'
    ],
)
