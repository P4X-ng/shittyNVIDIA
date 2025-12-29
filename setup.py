"""
Setup script for shittyNVIDIA
The worst NVIDIA driver ever - works with 0 nvidia devices
"""

from setuptools import setup, find_packages
import os

# Read the long description from README
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

setup(
    name='shitty-nvidia',
    version='0.0.0',
    description='The worst NVIDIA driver ever - works with 0 nvidia devices',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='shittyNVIDIA Contributors',
    author_email='',
    url='https://github.com/P4X-ng/shittyNVIDIA',
    packages=find_packages(),
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: System :: Hardware',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='nvidia gpu driver humor satire',
    license='MIT',
    scripts=['install-nvidia-compat.sh'],
    entry_points={
        'console_scripts': [
            'shitty-nvidia-info=shitty_nvidia:get_driver_info',
        ],
    },
)
