import rsa
import urllib
import zoo
import base64

def ChangeThredds(conf,inputs,outputs):
	crypto = inputs["url"]["value"]
	
	privatefile = open('privateKey.pem')
	keydata = privatefile.read()
	privatekey = rsa.PrivateKey.load_pkcs1(keydata)
	unquote = base64.b16decode(crypto)

	newurl = rsa.decrypt(unquote,privatekey)

	ThreddServer = open('ThreddServer','w')
	ThreddServer.write(newurl)

	return zoo.SERVICE_SUCCEEDED
