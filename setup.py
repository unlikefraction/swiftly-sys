from setuptools import setup, find_packages
import glob
import os

scripts = [f for f in glob.glob('scripts/unix/**/*', recursive=True) + glob.glob('scripts/windows/**/*', recursive=True) if os.path.isfile(f)]

setup(
    name='swiftly-sys',
    version='0.0.121',
    license='Apache2',
    packages=find_packages(),
    include_package_data=True,
    scripts=scripts,
    description = 'Do what you\'re good at; writing code. Swiftly handle the rest',
    long_description='''
    Swiftly let's you focus on building amazing products. Swiftly makes sure your entire code scales, while keeping the code so maintainable. No spaghetti code, ever!\n
    Read the docs at: https://swiftly-sys.tech
    ''',
    author = 'Shubham Gupta',
    author_email = 'shubhastro2@gmail.com',
    url = 'https://github.com/brainspoof/swiftly-sys',
    keywords = ['python project', 'project management', 'code management', 'project building', 'python project managment', 'organized project'],
    install_requires=[
            'questionary',
            'requests',
            'pipdeptree',
            'jinja2',
        ],
)