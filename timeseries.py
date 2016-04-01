import urllib, urllib2, base64, json, datetime

# Fill in your API credentials
API_ID 				= '3HUOQWVK0WDIH3N1I4CZXVESB'
API_SECRET 			= 'sZTgiwMeeAtGRnvtmHGKAEYYs+Rr/uBh1djYAxiUwoM'

# Generate base64 encoded authorization string
basicAuthString 	= base64.encodestring('%s:%s' % (API_ID, API_SECRET)).replace('\n', '')

# Function to request data from API
def apiRequest (url, params = {}):

	# Encode optional parameters
	encodedParams 		= urllib.urlencode(params)

	# Set API endpoint
	request 			= urllib2.Request(url + '?' + encodedParams)

	# Add authorization header to the request
	request.add_header("Authorization", "Basic %s" % basicAuthString)	

	try:
		response 		= urllib2.urlopen(request)
		return response.read()
	except urllib2.HTTPError, err:
		if err.code == 401:
			print "Error: Invalid API credentials";
			quit()
		elif err.code == 404:
			print "Error: The API endpoint is currently unavailable";
			quit()
		else:
			print err
			quit()

# Specify station id
stationId 				= 'TA00058'

# Generate timestamp of 48 hours ago (e.g. 2016-03-25T14:00)
startDate 				= datetime.datetime.strftime(datetime.datetime.utcnow()-datetime.timedelta(2),'%Y-%m-%dT%H:%M')

# Request stations from API
response 				= apiRequest("https://tahmoapi.mybluemix.net/v1/timeseries/" + stationId + "/hourly", { 'startDate': startDate })
decodedResponse			= json.loads(response)

# Check if API responded with an error
if(decodedResponse['status'] == 'error'):
	print "Error:", decodedResponse['error']

# Check if API responded with success
elif(decodedResponse['status'] == 'success'):

	# Print the amount of stations that were retrieved in this API call
	print "API call success:", "Station", decodedResponse['station']['id'], decodedResponse['station']['name'], "timeseries retrieved"
	print "Timeseries available for ", ", ".join(decodedResponse['station']['variables'])

	# Loop through temperature timeseries and print values
	try:
		if decodedResponse['timeseries']['temperature']:
			print "\nTemperature measurements during last two days: "

			for timestamp, value in sorted(decodedResponse['timeseries']['temperature'].items()):
				print timestamp, value

	except:
		print "Temperature timeserie starting at " + startDate + " unavailable"
		quit()