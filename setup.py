from setuptools import setup, find_packages

metadata = {
    'name': 'WikimediaScraper',
    'version': '0.1',
    'description': 'Scrap wikimedia commons images',
    'author': 'NaN',
    'author_email': 'NaN'
}
packages = find_packages()
dependencies = ['certifi==2022.12.7',
                'charset-normalizer==3.1.0',
                'colored==1.4.4',
                'Faker==17.6.0',
                'idna==3.4',
                'python-dateutil==2.8.2',
                'requests==2.28.2',
                'six==1.16.0',
                'tenacity==8.2.2',
                'termcolor==2.2.0',
                'urllib3==1.26.14',
                'aiofiles==23.1.0',
                'aiohttp==3.8.4',
                'aiosignal==1.3.1',
                'async-timeout==4.0.2'
                'attrs==22.2.0',
                'chardet==4.0.0',
                ]
setup(
    name=metadata['name'],
    version=metadata['version'],
    description=metadata['description'],
    author=metadata['author'],
    author_email=metadata['author_email'],
    packages=packages,
    install_requires=dependencies,
)
