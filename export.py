import urllib, urllib2, base64, json, csv, os

# Fill in your API credentials
API_ID 				= '3HUOQWVK0WDIH3N1I4CZXVESB'
API_SECRET 			= 'sZTgiwMeeAtGRnvtmHGKAEYYs+Rr/uBh1djYAxiUwoM'

# Generate base64 encoded authorization string
basicAuthString 	= base64.encodestring('%s:%s' % (API_ID, API_SECRET)).replace('\n', '')

# Set startDate and endDate of timeseries
# Could be an empty string to start with first measurement, or any datetime string according to the ISO-8601 standard
startDate 				= '2016-06-30'
endDate 				= '2016-07-11'

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

# Request stations from API
response 				= apiRequest("https://tahmoapi.mybluemix.net/v1/stations")
decodedResponse			= json.loads(response)

# Check if API responded with an error
if(decodedResponse['status'] == 'error'):
	print "Error:", decodedResponse['error']

# Check if API responded with success
elif(decodedResponse['status'] == 'success'):

	# Print the amount of stations that were retrieved in this API call
	print "API call success:", len(decodedResponse['stations']), "stations retrieved"

	# Loop through received stations
	for station in decodedResponse['stations']:

		print "\n";

		# Keep track of last measurement that is written to the CSV file
		lastMeasurement 		= startDate;

		# Set default values for station properties
		station.setdefault('id', 'unkown')
		station.setdefault('name', 'unkown')
		station.setdefault('lastMeasurement', '')

		# Create folder for this station if it doesn't exist yet
		if not os.path.exists(station['id']):
		    os.makedirs(station['id'])

		print "Start receiving timeseries for station", station['id']

		# Maximum attempts as a security measure for the while loop
		attempt 	= 0;

		# The timeseries call currently only returns 4 weeks of data, therefore a while loop is used until the last data is retrieved (maximum attempts accounts for 2 years of data)
		# This will be improved in future versions of the API
		while ((lastMeasurement < station['lastMeasurement'][0:13] and lastMeasurement < endDate) and attempt < (2 * 4 * 13)):

			attempt 				+= 1;

			# Request timeseries for specific station
			tsResponse 				= apiRequest("https://tahmoapi.mybluemix.net/v1/timeseries/" + station['id'] + "/", { 'startDate': lastMeasurement, 'endDate': endDate })
			decodedTsResponse		= json.loads(tsResponse)

			# Check if API responded with an error
			if(decodedTsResponse['status'] == 'error'):
				print "Error:", decodedTsResponse['error']

			# Check if API responded with success
			elif(decodedTsResponse['status'] == 'success'):

				# Print success message
				print "API call success: timeseries for ", station['id'], "startdate ", lastMeasurement

				for variable in decodedTsResponse['station']['variables']:

					# Set filename
					fileName 	= station['id'] + '/' + station['id'] + '_' + variable + '.csv'

					# Determine file write mode (overwrite file with first data, later requests append it to the file)
					if attempt == 1:
						fileMode 	= 'wb'
					else:
						fileMode 	= 'ab'

					# Generate CSV file to export data
					with open(fileName, fileMode) as csvFile:

						# Create csv writer object
						writer 			= csv.writer(csvFile)
						line 			= 0;

						try:
							# Loop through variable specific timeseries
							for timestamp, value in sorted(decodedTsResponse['timeseries'][variable].items()):

								line 					+= 1 

								# Skip first measurement if it isn't the first request to prevent duplicates
								if line > 1 or attempt == 1:
									# Write value to csv file
									writer.writerow([timestamp] + [value])

								# Update lastMeasurement variable of csv file
								if timestamp > lastMeasurement:
									lastMeasurement 	= timestamp

						except:
							print "Could not process variable ", variable
