from setuptools import setup

setup(
    name='pyntcloud',
    version='0.1',
    description='Point cloud operations in Python',
    url='https://github.com/daavoo/pyntcloud',
    author='David de la Iglesia Castro',
    author_email='daviddelaiglesiacastro@gmail.com',
    license='HAKUNAMATATA',
    packages=['pyntcloud',
              "pyntcloud.filters",
              "pyntcloud.geometry",
              "pyntcloud.io",
              "pyntcloud.plot",
              "pyntcloud.ransac",
              "pyntcloud.scalar_fields",
              "pyntcloud.structures",
              "pyntcloud.utils"],
    keywords=[
        "point cloud",
        "3D"
    ],
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
    ],
    classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Education",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: Hakuna Matata",
            "Natural Language :: Galician",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Mathematics",
            "Topic :: Scientific/Engineering :: Information Analysis",
            ],
    
    )
