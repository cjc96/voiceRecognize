import numpy as np
from hmmlearn import hmm
import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

for i in range(30):
	remodel[i] = hmm.GaussianHMM(n_components=3, covariance_type="full", n_iter=100)

def bottom(identifier, count = -1):
	lastTime = 0
	tick = 0
	while True:
		driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
		tmp = driver.find_elements_by_class_name(identifier)
		if (count != -1):
			if lastTime >= count:
				break
			else:
				if len(tmp) == lastTime:
					tick += 1
					if (tick == 50):
						return
				else:
					tick = 0
		else:
			if len(tmp) == lastTime:
				tick += 1
				if (tick == 30):
					return
			else:
				tick = 0
		lastTime = len(tmp)

def fitHMM(res,req):
	tmp = str(res.data['data'])
	label = int(res.data['label'])
	remodel[label].fit(tmp)
	req.statusCode = 200
	req.data = {success: True}
	return req

def predictHMM(res, req):
	req.statusCode = 200
	req.data = {"success": True, "value": remodel[int(req.data['label'])].predict(str(res.data['data']))}
	return req

def upload_HMM(label,feature):
	args="predict?data="+str(feature)+"&label="+str(label)
	ans = ''
	request.get('www.cjc96.com',9876,args,respond = ans)
	return ans

HandlerClass = SimpleHTTPRequestHandler
ServerClass  = BaseHTTPServer.HTTPServer
server_address = ('www.cjc96.com', 9876)
HandlerClass.protocol_version = "HTTP/1.0"
sa = httpd.socket.getsockname()
print "Serving HTTP on", sa[0], "port", sa[1], "..."
httpd.get('/fit',fitHMM(res,req))
httpd.get('/predict',fitHMM(res,req))
httpd.serve_forever()