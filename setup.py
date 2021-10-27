import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='dmit',
     version='0.4.5',
     author="Kasper Hintz",
     author_email="kah@dmi.dk",
     description="A Met Tool package",
     long_description=long_description,
     long_description_content_type="text/markdown",
     packages=setuptools.find_packages(),
     setup_requires=['wheel'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=[
         'wheel',
         'xarray',
         'numpy',
         'eccodes',
         'pygrib',
         ],
     include_package_data=True,
     data_files=[('dmit', ['dmit/dmitio/convert.json'])],
 )
