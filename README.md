# AETrackRSS #

Simple script that runs on Google App Engine and keeps track of RSS subscribers and file downloads for a podcast.

**Notes**

* This script should be used as the URL for the RSS feed of the podcast.
* If the request includes the parameter _file=filename.mp3_ the script will log the file access and return a redirect to get the actual file.
* If the request does not include any parameters the access will be logged and the user will be forwarded to the full RSS feed.
* This is a rough sketch of an idea for this program. It is far from finished. This may be a horrible way to track these statistics so I make no promises if you use this script.

**To Do**

* The admin code doesn't cache results so it must calculate the results every time the script is run. This could take a lot of time and use a good bit of AE resources if the script tracks a lot of data.
* This currently uses GQL and the default AE data store. Not sure this is the best idea but it is quick.
* Admin console doesn't require admin authentication.
* The admin console could show a lot more data and be a lot prettier.