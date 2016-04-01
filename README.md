# API V1 Python examples
This git contains examples on how to use the TAHMO API v1 in the python.

There are currently three examples available:

* **stations.py**: Retrieves all stations that your account has access to and export the station id, station name, location and last measurement information to a CSV file.

* **timeseries.py**: Retrieve timeseries of the last 48 hours of a specific station.

* **export.py**: Export all timeseries of all stations to CSV files, beginning at a specified date.



## Authorization
The python examples contain API credentials of a demo account which only has access to two TAHMO stations. Please update these to your own API credentials in order to access all your available stations.

## Additional information
Additional information on how to use the API, available endpoints, units etc is presented in the API documentation.
For questions please send an email to H.F.Hagenaars@student.tudelft.nl.