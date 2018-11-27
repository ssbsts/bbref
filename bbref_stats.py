#!/usr/bin/python

import sys
from bs4 import BeautifulSoup
import urllib2
import csv
import fileinput
import argparse
import time
import random

parser = argparse.ArgumentParser(description='Get some stats')
parser.add_argument('-year', type=str, required=True, help='year to get games for')
args = parser.parse_args()

tmp_file='temp_out.csv'
output='stats_{}.csv'.format(args.year)
url_file='test.html'
offset=0
f = open(tmp_file, 'wb')

while True:
    sleep_time = random.randint(5, 60)
    url='https://www.basketball-reference.com/play-index/pgl_finder.cgi?request=1&player_id=&match=game&year_min={}&year_max={}&age_min=0&age_max=99&team_id=&opp_id=&season_start=1&season_end=-1&is_playoffs=N&draft_year=&round_id=&game_num_type=&game_num_min=&game_num_max=&game_month=&game_day=&game_location=&game_result=&is_starter=&is_active=&is_hof=&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&c1stat=&c1comp=&c1val=&c1val_orig=&c2stat=&c2comp=&c2val=&c2val_orig=&c3stat=&c3comp=&c3val=&c3val_orig=&c4stat=&c4comp=&c4val=&c4val_orig=&is_dbl_dbl=&is_trp_dbl=&order_by=pts&order_by_asc=&offset={}'.format(args.year,args.year,offset)
    print(url)
    retry = 0
    while True:
        try:
            page = urllib2.urlopen(url).read()
        except HTTPError as e:
            if e.code == 502:
                time.sleep(sleep_time)
                count += 1
                continue
            if retry >= 5:
                sys.exit(1)
        break				
        
    soup    = BeautifulSoup(page, features="html.parser")
    csvout  = csv.writer(f)
    
    for table in soup.findAll('table'):
        for row in table.findAll('tr'):
            csvout.writerow([tr.text for tr in row.findAll('td')])
    f.close()
    f = open(output, 'a')
    
    for line in fileinput.FileInput(tmp_file,inplace=1):
        if line.rstrip():
            f.write(line)
    
    if "Next page" in page:
        offset += 100
        time.sleep(sleep_time)
        continue
    break
		
sys.exit(0)	