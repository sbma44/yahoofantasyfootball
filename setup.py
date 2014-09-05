from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='yahoofantasyfootball',
      version='0.3',
      description='Web scraper for Yahoo! Fantasy Football data. Not affiliated with or endorsed by Yahoo!',
      url='http://github.com/sbma44/yahoofantasyfootball',
      author='Tom Lee',
      author_email='thomas.j.lee@gmail.com',
      license='MIT',
      packages=['yahoofantasyfootball'],
      install_requires=[
          'BeautifulSoup', 
          'mechanize',
          'selenium',
      ],      
      zip_safe=False)
