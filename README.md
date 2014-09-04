yahoofantasyfootball
====================

An unofficial web scraper for Yahoo! Fantasy Football (YFF) data. Not affiliated with or endorsed by Yahoo! in any way.

[![Build Status](https://travis-ci.org/sbma44/yahoofantasyfootball.svg?branch=master)](https://travis-ci.org/sbma44/yahoofantasyfootball)

Installation
------------
Should be as simple as `pip install yahoofantasyfootball`. Alternately, `python setup.py install`.

Requirements
------------
In addition to the libraries listed in requirements.txt, this library relies upon the presence of [PhantomJS](http://phantomjs.org/). Get it, install it, love it.

Usage
-----
```
import yahoofantasyfootball

LEAGUE_URL = 'http://football.fantasysports.yahoo.com/f1/123456'
YAHOO_USERNAME = 'foo'
YAHOO_PASSWORD = 'bar' # please be careful not to publish your password

yff = yahoofantasyfootball.YahooFantasyFootball(LEAGUE_URL, YAHOO_USERNAME, YAHOO_PASSWORD)
yff.refresh() # logs in, pulls down league HTML
yff.process() # parses HTML, puts data into useful variables

print yff.scores, yff.standings, yff.matchups
```

Notes
-----
* This library relies upon screen scraping, which is an inherently unreliable technique. YFF has held its templates relatively steady between the 2013-2014 and 2014-2015 seasons, but that could change at any moment. They should really consider making a non-terrible API.

* I have no idea if Yahoo! supports non-ASCII team names, but if they do, they will probably not be collected correctly, as I am stripping out Unicode to get rid of the silly trophy icons they put next to team names.

* There is a frightening amount of additional data available through the YFF interface. Pull requests are welcome! However, it is unlikely that YFF is legally able to relay scores or player information to third parties. Consequently I am unlikely to accept PRs that collect individual player stats or other information that the NFL might have IP rights to. User-generated content and game outcome data is all fair game, though, I think.

Contact
-------
thomas.j.lee (at) google's very popular webmail service
