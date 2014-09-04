from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='yahoofantasyfootball',
      version='0.1',
      description='Web scraper for Yahoo! Fantasy Football data. Not affiliated with Yahoo!',
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
      scripts=[
        'bin/pwm_calibrate',
      ],
      zip_safe=False)
