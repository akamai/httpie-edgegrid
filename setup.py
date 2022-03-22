from setuptools import setup

try:
    import multiprocessing
except ImportError:
    pass

setup(
    name='httpie-edgegrid',
    description='Edgegrid plugin for HTTPie.',
    python_requires=">=2.7.10",
    long_description=open('README.rst').read().strip(),
    version='1.0.2',
    author='Kirsten Hunter',
    author_email='khunter@akamai.com',
    license='Apache 2.0',
    url='https://github.com/akamai/httpie-edgegrid',
    download_url='https://github.com/akamai/httpie-edgegrid',
    maintainer_email='dl-devexp-eng@akamai.com',
    py_modules=['httpie_edgegrid'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_oauth1 = httpie_edgegrid:EdgeGridPlugin'
        ]
    },
    install_requires=[
        'httpie == 3.1.0',
        'edgegrid-python == 1.2.1',
        'pyOpenSSL == 22.0.0'
    ],

)
