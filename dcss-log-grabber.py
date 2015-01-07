import urllib2
import pickle
import threading

logfilenames = ["http://crawl.akrasiac.org/logfile15",
		"http://crawl.akrasiac.org/logfile14",
		"http://crawl.akrasiac.org/logfile-git",
		"http://crawl.develz.org/allgames-0.14.txt",
		"http://crawl.develz.org/allgames-0.15.txt",
		"http://crawl.develz.org/allgames-svn.txt",
		"http://dobrazupa.org/meta/0.15/logfile",
		"http://dobrazupa.org/meta/0.14/logfile",
		"http://dobrazupa.org/meta/git/logfile",
		"http://crawl.lantea.net/crawl/meta/0.15/logfile",
		"http://crawl.lantea.net/crawl/meta/0.14/logfile",
		"http://crawl.lantea.net/crawl/meta/git/logfile",
		"http://kr.dobrazupa.org/www/0.15/logfile",
		"http://kr.dobrazupa.org/www/0.14/logfile",
		"http://kr.dobrazupa.org/www/trunk/logfile",
		"http://crawl.berotato.org/crawl/meta/0.15/logfile",
		"http://crawl.berotato.org/crawl/meta/0.14/logfile",
		"http://crawl.berotato.org/crawl/meta/git/logfile",
		"http://crawl.xtahua.com/crawl/meta/0.15/logfile",
		"http://crawl.xtahua.com/crawl/meta/0.14/logfile",
		"http://crawl.xtahua.com/crawl/meta/git/logfile",
		"https://crawl.project357.org/dcss-logfiles-trunk",
		"https://crawl.project357.org/dcss-logfiles-0.15"]



logfiles = {}
thrlist = []
thrlock = threading.Lock()

def download(urlname):
	print "Downloading ... ", urlname
	try:
		tmp = urllib2.urlopen(urlname)
		tmp2 = tmp.read()
		add_to_logfilesdict(urlname, tmp2)
		tmp.close()
	except Exception as msg:
		print "unable to download", str(msg)
	print "Done ..", urlname

def add_to_logfilesdict(urlname, data):
	thrlock.acquire()
	logfiles[urlname] = data
	thrlock.release()

for urlname in logfilenames:
	tmp = threading.Thread(target=download, args=(urlname,))
	tmp.start()
	thrlist.append(tmp)

for thr in thrlist:
	thr.join()

with open("dcsslogs.pickle", "w") as f:
	pickle.dump(logfiles, f)



	    
	    
