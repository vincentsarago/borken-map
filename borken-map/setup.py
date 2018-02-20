
from setuptools import setup

# Parse the version from the poster module.
with open('borken_map/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue


setup(name='borken_map',
      version=version,
      python_requires='>=3',
      description=u"do the job",
      long_description=u"do my job",
      author=u"",
      author_email='',
      license='BSD',
      packages=['borken_map'],
      include_package_data=True,
      package_data={'borken_map': [
        'data/mapbox.png',
        'data/mb_osm.png',
        'data/mb_dg.png']},
      install_requires=[
        'tweepy',
        'Pillow',
        'requests',
        'supermercado',
        'rasterio[s3]>=1.0a12'
      ],
      zip_safe=False,
      entry_points="""
      [console_scripts]
      borken=borken_map.cli.cli:create
      """)
