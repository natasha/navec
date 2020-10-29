
from setuptools import setup, find_packages


with open('README.md') as file:
    description = file.read()


with open('requirements/main.txt') as file:
    requirements = [_.strip() for _ in file]


setup(
    name='navec',
    version='0.10.0',
    description='Compact high quality word embeddings for russian language',
    long_description=description,
    long_description_content_type='text/markdown',
    url='https://github.com/natasha/navec',
    author='Alexander Kukushkin',
    author_email='alex@alexkuk.ru',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='embeddings, word2vec, glove, nlp, russian, quantization',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'navec-train=navec.train.ctl.__main__:main'
        ]
    }
)

