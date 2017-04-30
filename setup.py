from setuptools import setup, find_packages

setup(
    name='pyntcloud',
    version='8999',
    description='Python library for working with 3D point clouds.',
    url='https://github.com/daavoo/pyntcloud',
    author='David de la Iglesia Castro',
    author_email='daviddelaiglesiacastro@gmail.com',
    license='HAKUNAMATATA',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "ipython",
        "pytest",
        "matplotlib",
        "python-lzf",
        "numba",
        "laspy"
    ],

)
