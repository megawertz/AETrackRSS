import webapp2
import datetime
from google.appengine.ext import db
from google.appengine.api import users

FILEREQUEST_BASE_URL = "http://www.megawertz.com/podcastfiles/"

# Data model for logging client information
class LogData(db.Model):
	date = db.DateProperty()
	ip = db.StringProperty()
	file = db.StringProperty()

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Main")
		
class TrackRSS(webapp2.RequestHandler):
	def get(self):
		# Get the file name if present. Format: file=my.mp3
		fileRequest = str(self.request.get("file"))

		# Format the data for storage 
		# If the file is null, the user viewed the full RSS
		# This should give some idea of subscribers vs. downloads
		ld = LogData(date=datetime.datetime.now().date(), 
					 ip=self.request.remote_addr,
					 file = fileRequest)
		ld.put()

		# If the fileRequest is not null get a specific file
		if fileRequest:		 	
			self.redirect(FILEREQUEST_BASE_URL + fileRequest)
		else:
			self.redirect("http://www.megawertz.com/podcast.rss")
								
class Admin(webapp2.RequestHandler):
	def get(self):
		# Get each file the db has seen 
		files = db.GqlQuery("SELECT DISTINCT file FROM LogData");

		# Now add up the total downloads for each file
		# Results should be cached to avoid the cost of resubmitting within a given period
		self.response.out.write("<h1>RSS Download Stats</h1>")
		self.response.out.write("<table border=2 cellpadding=5><tr><th>File Name</th><th>Total Downloads</th></tr>");
		
		totalRSS = 0;
		totalFiles = 0;
		
		for p in files.run():
			downloadCount = db.GqlQuery("SELECT __key__ FROM LogData WHERE file = :1", p.file);
			totalDownloads = downloadCount.count();
			self.response.out.write("<tr><td>" + p.file + "</td><td align=center>" + str(totalDownloads) + "</td></tr>")
			if p.file:
				totalFiles = totalFiles + totalDownloads;
			else:
				totalRSS = totalRSS + totalDownloads;
				
		self.response.out.write("</table>");
		self.response.out.write("<br><b>Total File Downlads: " + str(totalFiles) + "<br>Total RSS Hits: " + str(totalRSS) + "</b>" );

app = webapp2.WSGIApplication( [('/', MainPage),
								('/trackrss', TrackRSS),
								('/admin', Admin)],
								debug=False)
								