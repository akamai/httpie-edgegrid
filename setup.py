from setuptools import setup

try:
    import multiprocessing
except ImportError:
    pass

setup(
    name='httpie-edgegrid',
    description='Edgegrid plugin for HTTPie.',
    python_requires=">=3.7",
    long_description=open('README.md').read().strip(),
    version='2.1.0',
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
