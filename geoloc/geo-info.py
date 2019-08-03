import json
import re
import socket
import sys
import time
import ipapi # https://github.com/ipapi-co/ipapi-python
import sqlite3 # https://docs.python.org/3/library/sqlite3.html

### Disable buffering
class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)
sys.stdout = Unbuffered(sys.stdout)

### -----------------------------------
### Helper functions
### -----------------------------------

def get_top_sites():
	top_sites = open("alexa_top_hu.json","r",encoding='utf-8').read()
	top_sites = re.sub(",[ \t\r\n]+\]", "]", top_sites) # remove trailing commas
	top_sites = json.loads( top_sites ) 
	
	return [ 
		{
			"rank": i[0],
			"domain": i[1],
			"Description": i[2],
			"Daily Time on Site": i[3],
			"Daily Pageviews per Visitor": i[4],
			"% of Traffic From Search": i[5],
			"Total Sites Linking In": i[6],
		}
		for i in top_sites[1:]
	]

def create_db(c):
	sql_create = '''CREATE TABLE sites (
		rank INTEGER,
		domain TEXT,
		
		description TEXT,
		daily_time_on_site TEXT,
		daily_pageviews_per_visitor TEXT,
		percent_of_traffic_from_search TEXT,
		total_sites_linking_in TEXT,
		
		ip TEXT,
		
		city TEXT,
		region TEXT,
		region_code TEXT,
		country TEXT,
		
		country_name TEXT,
		
		continent_code TEXT,
		
		in_eu TEXT,
		
		postal TEXT,
		latitude TEXT,
		longitude TEXT,
		timezone TEXT,
		utc_offset TEXT,
		country_calling_code TEXT,
		currency TEXT,
		languages TEXT,
		asn TEXT,
		org TEXT
		
	)'''
	
	if sql_create != c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='sites';").fetchone()[0] :
		print('Previous datas:')
		for row in c.execute('SELECT * FROM sites '):
			print( row )
		print('Reset table')
		c.execute('DROP TABLE IF EXISTS sites')
		c.execute(sql_create)
	print( 'Current data rows count: ', c.execute("SELECT COUNT(*) FROM sites").fetchone()[0] )

def getIP(d):
	"""
	This method returns the first IP address string
	that responds as the given domain name
	"""
	try:
		return socket.gethostbyname(d)
	except Exception:
		print('getIP Exception for: ' + d)
		#raise
		return False

def get_geo_info(ip):
	# from requests import get
	# loc = get('http://ip-api.com/json/'+ip])
	# print( repr( loc.json() ).encode('utf-8') )
	
	mockloc = {'ip': '216.58.214.206', 'city': 'Mountain View', 'region': 'California', 'region_code': 'CA', 'country': 'US', 'country_name': 'United States', 'continent_code': 'NA', 'in_eu': False, 'postal': '94043', 'latitude': 37.4043, 'longitude': -122.0748, 'timezone': 'America/Los_Angeles', 'utc_offset': '-0700', 'country_calling_code': '+1', 'currency': 'USD', 'languages': 'en-US,es-US,haw,fr', 'asn': 'AS15169', 'org': 'Google LLC'}
	
	try:
		#geo_info = mockloc
		geo_info = ipapi.location( ip )
		if 'error' in geo_info and geo_info['error']==True:
			print('ipapi error for: ' + ip + ' , reason: ' + geo_info['reason'])
			return False
		return geo_info
	except Exception:
		print('Exception when ipapi for: ' + ip)
		return False

### -----------------------------------
### 
### -----------------------------------

conn = sqlite3.connect('sites.sqlite3')
c = conn.cursor()

create_db(c)

top_sites = get_top_sites()

# populate domains
for site in top_sites:
	if not c.execute("SELECT * FROM sites WHERE rank=? AND domain=? ", (site['rank'], site['domain']) ).fetchone():
		print('New site: ', site['rank'], site['domain'])
		c.execute("INSERT INTO sites (rank, domain) VALUES ( ?, ?)", (site['rank'], site['domain']))
print('\n')

# resolve domains to ips
for (domain,) in c.execute("SELECT domain FROM sites WHERE ip IS NULL ").fetchall():
	#print('Lookup ', domain)
	continue
	ip = getIP( domain )
	if ip:
		c.execute("UPDATE sites SET ip=? WHERE domain=? ", (ip, domain))
	else:
		www_domain = 'www.' + domain
		ip = getIP( www_domain )
		if ip:
			#c.execute("UPDATE sites SET domain=?, ip=? WHERE domain=? ", (www_domain, ip, domain))
			c.execute("UPDATE sites SET ip=? WHERE domain=? ", (ip, domain))
print('\n')

# get information about the ips
for (ip,) in c.execute("SELECT ip FROM sites WHERE ip IS NOT NULL AND country_name IS NULL ").fetchall():
	continue
	geo_info = get_geo_info( ip )
	if geo_info:
		c.execute('''UPDATE sites SET
			 city=:city,
			 region=:region,
			 region_code=:region_code,
			 country=:country,
			 country_name=:country_name,
			 continent_code=:continent_code,
			 in_eu=:in_eu,
			 postal=:postal,
			 latitude=:latitude,
			 longitude=:longitude,
			 timezone=:timezone,
			 utc_offset=:utc_offset,
			 country_calling_code=:country_calling_code,
			 currency=:currency,
			 languages=:languages,
			 asn=:asn,
			 org=:org
		WHERE ip=:ip ''', geo_info)
print('\n')


print('\n')
# , CASE WHEN in_eu THEN 'IN_EU' ELSE 'NOT_EU' END
for row in c.execute("SELECT COUNT(*), org, asn, country_name FROM sites WHERE ip IS NOT NULL AND country_name IS NOT NULL GROUP BY org, asn, country_name, in_eu ORDER BY org "):
	print( '|'.join([str(i) for i in row]))
	#print( row )

print('\n')
for row in c.execute("SELECT org, COUNT(*) FROM sites WHERE ip IS NOT NULL AND country_name IS NOT NULL GROUP BY org ORDER BY COUNT(*) DESC "):
	print( '|'.join([str(i) for i in row]))

print('\n')
for row in c.execute('SELECT COUNT(*) FROM sites WHERE ip IS NOT NULL AND country_name IS NOT NULL '):
	print( row )
for row in c.execute('SELECT COUNT(*) FROM sites WHERE ip IS NOT NULL '):
	print( row )
for row in c.execute('SELECT COUNT(*) FROM sites WHERE country_name IS NOT NULL '):
	print( row )

conn.commit() # Save (commit) the changes
conn.close()


print("Finished!")
