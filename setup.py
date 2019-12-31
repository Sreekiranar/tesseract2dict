from setuptools import setup

with open('README.md','r') as f:
    long_description = f.read()


setup(name='tesseract2dict',
      version='1.0',
      description='enter the package description',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='enter the url',
      authors='Sreekiran A R, Anil Prasad M N',
      author_email='sreekiranar@gmail.com, anilprasadmn@gmail.com',
      license='MIT',
      packages=['tesseract2dict'],
      install_requires=['beautifulsoup4', 'MakeTreeDir', 'numpy', 'opencv-python', 'pandas', 'pytesseract'], include_package_data=True,
      zip_safe=False)
