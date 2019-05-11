

#import sys, os
#sys.path = [os.path.expanduser('~/.local/lib/python2.7/site-packages')] + sys.path
#print(sys.path)

from tranco import Tranco

from OpenWPM.automation import CommandSequence, TaskManager

# The list of sites that we wish to crawl
NUM_BROWSERS = 3
sites = [
	'http://www.example.com',
	#'http://www.princeton.edu',
	#'http://citp.princeton.edu/',
	#'https://index.hu/gazdasag/2019/05/01/nettolotto_17/'
	]

sites = map(lambda domain: 'http://'+domain, Tranco().list().top(10) )

# Loads the manager preference and 3 copies of the default browser dictionaries
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in range(NUM_BROWSERS):
	# Launch browsers headless
	browser_params[i]['headless'] = True
	
	# Record HTTP Requests and Responses
	browser_params[i]['http_instrument'] = True

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/openwpm_results/'
manager_params['log_directory'] = '~/openwpm_results/'

# Instantiates the measurement platform
print('Starting the manager...')
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites with all browsers simultaneously
print('Visiting the sites...')
for site in sites:
	command_sequence = CommandSequence.CommandSequence(site, reset=True)
	
	# Start by visiting the page
	command_sequence.get(sleep=5, timeout=60)
	
	#command_sequence.save_screenshot('screenshot')
	
	# index='**' synchronizes visits between the three browsers
	manager.execute_command_sequence(command_sequence)#, index='*')

# Shuts down the browsers and waits for the data to finish logging
manager.close()

