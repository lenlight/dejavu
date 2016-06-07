import time, sys
import urllib2
import warnings
import json
warnings.filterwarnings("ignore")

from dejavu import Dejavu
from dejavu.recognize import FileRecognizer

# load config from a JSON file (or anything outputting a python dictionary)
with open("dejavu.cnf.SAMPLE") as f:
    config = json.load(f)

	# create a Dejavu instance
	djv = Dejavu(config)

url = "http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio1_mf_p"
print ("Connecting to "+url)
while True:
    response = urllib2.urlopen(url, timeout=10.0)
    fname = "Radio.wav"
    f = open(fname, 'wb')
    block_size = 1024
    print ("Recording roughly 10 seconds of audio Now - Please wait")
    limit = 10
    start = time.time()
    while time.time() - start < limit:
        try:
            audio = response.read(block_size)
            if not audio:
                break
            f.write(audio)
            sys.stdout.write('.')
            sys.stdout.flush()
        except Exception as e:
            print ("Error "+str(e))
    f.close()
    sys.stdout.flush()
    print("")
    print ("10 seconds from "+url+" have been recorded in "+fname)

    # Recognize audio from a file
	song = djv.recognize(FileRecognizer, fname)
	print "From file: %s\n" % song