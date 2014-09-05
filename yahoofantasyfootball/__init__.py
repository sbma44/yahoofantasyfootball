import sys
import os
import re
import pprint

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import cookielib

from BeautifulSoup import BeautifulSoup
from soupselect import select

import time

class YahooFantasyFootball(object):
    """ 
    Collects information from Yahoo Fantasy Football

    >>> y = YahooFantasyFootball()
    >>> y.refresh()
    
    >>> len(y.scores) > 0
    True
    
    >>> len(y.standings) > 0
    True
    
    >>> len(y.matchups) > 0
    True

    """
    def __init__(self, league_url=None, username=None, password=None):
        super(YahooFantasyFootball, self).__init__()        

        self.league_url = league_url
        self.username = username
        self.password = password

        if league_url is None and username is None and password is None:
            self.league_url = os.environ['YAHOO_LEAGUE_URL']
            self.username = os.environ['YAHOO_USERNAME']
            self.password = os.environ['YAHOO_PASSWORD']                    

        self.phantom = None    
        self.last_refresh = None    

    def initialize_phantomjs(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
            "(KHTML, like Gecko) Chrome/15.0.87"
        )
        self.phantom = webdriver.PhantomJS(desired_capabilities=dcap)
        self.phantom.set_window_size(1280, 1024)  

    def _integerize(self, text):
        """
        >>> y = YahooFantasyFootball()
        >>> y._integerize('(123)')
        123
        >>> y._integerize('0-1-2')
        12
        >>> y._integerize('-')
        0
        """
        if text.strip() == '-':
            return 0
        else:
            return int(re.sub('[^\d]', '', text))

    def _remove_nonascii(self, s):
        return "".join(filter(lambda x: ord(x)<128, s))

    def refresh(self):
        self._pull_html()
        self._process_html()

    def _pull_html(self):
        """ Refreshes HTML collected from league page, logging in if necessary """
        
        if self.phantom is None:
            self.initialize_phantomjs()

        self.phantom.get(self.league_url)
        
        if ('login' in self.phantom.title.lower()) or ('sign in to yahoo' in self.phantom.title.lower()):
        
            submit_control = None
            login_control = None
            password_control = None

            for e in self.phantom.find_elements_by_tag_name('input'):
                
                # login
                if e.get_attribute('name') in ('login', 'id'):
                    login_control = e
                    e.send_keys(self.username)
                
                # password
                if e.get_attribute('name') in ('passwd', 'password'):
                    password_control = e
                    e.send_keys(self.password)
                
                # 'remember me'
                if e.get_attribute('name') in ('persistent',):
                    if e.get_attribute('value')=='y':
                        self.phantom.get_element_by_id('pLabelC').click()
                
                # mobile login form?
                if e.get_attribute('name') in ('.save', '__submit'):
                        submit_control = e

            # ugh it's a <button>
            if submit_control is None:
                for e in self.phantom.find_elements_by_tag_name('button'):
                    if e.get_attribute('name') in ('.save', '__submit'):
                        submit_control = e

            if submit_control is None:
                raise Exception('Submission control not found')
            if login_control is None:
                raise Exception('Username field control not found')
            if password_control is None:
                raise Exception('Password field control not found') 
            
            submit_control.click()
            time.sleep(5)     
                

        # wait for the html to settle down before storing it
        self.html = ''
        while self.phantom.page_source != self.html:
            time.sleep(10)
            self.html = self.phantom.page_source

        self.last_refresh = time.time()     

    def _process_html(self):
        """ Processes collected HTML """

        if self.last_refresh is None:
            raise Exception('Cannot process data prior to retrieving it (with refresh())')

        scores = {}
        matchups = []
        b = BeautifulSoup(self.html)
        for row in select(b, 'ul.List-rich li.Linkable'):
            matchup = []
            for player in select(row, 'div.Grid-h-mid'):
                score = select(player, 'div.Fz-lg')[0].getText()
                projected = select(player, 'div.F-shade')[0].getText()
                name = select(player, 'div.Fz-sm a')[0].getText()
                scores[name] = {'score': self._integerize(score), 'projected': self._integerize(projected)}                                
                matchup.append(name)
            matchups.append(matchup)

        self.scores = scores
        self.matchups = matchups

        standings = []
        cell_order = ('rank', 'name', 'record', 'points', 'points_against', 'streak', 'waiver', 'moves')
        text_cells = ('name', 'record')
        for row in select(b, 'table#standingstable tbody tr'):
            record = {}
            for (i, cell) in enumerate(select(row, 'td')):
                val = self._remove_nonascii(cell.getText())
                if cell_order[i] not in text_cells:
                    val = self._integerize(val)
                record[cell_order[i]] = val
            standings.append(record)

        self.standings = standings
    

    def get_score_differential(self, player):
        opponent = None
        for m in self.matchups:
            for (i, p) in enumerate(m):
                if p == player:
                    opponent = m[(i+1) % len(m)]        
        
        if opponent is None:
            raise Exception('Could not find player in matchups')

        return int(self.scores[player]['score']) - int(self.scores[opponent]['score'])

    def get_standing(self, player):
        for s in self.standings:
            if s.get('name')==player:
                return int(s.get('rank', 12))

if __name__ == '__main__':
    if '--show' in sys.argv:
        y = YahooFantasyFootball()
        y.refresh()

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(y.scores)
        pp.pprint(y.standings)
        pp.pprint(y.matchups)
        
    else:
        import doctest
        sys.exit(doctest.testmod()[0])

