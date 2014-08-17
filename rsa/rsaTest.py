import rsa
import urllib
import base64

def main():
	test = "http://115.146.84.143:8080"
	privatefile = open('privateKey.pem')
	keydata = privatefile.read()
	privatekey = rsa.PrivateKey.load_pkcs1(keydata)
	publicfile = open('publicKey.pem')
	pubdata = publicfile.read()
	pubkey = rsa.PublicKey.load_pkcs1(pubdata)
	
	crypto = rsa.encrypt(test,pubkey)
	newtest = rsa.decrypt(crypto,privatekey)
	print crypto
	urlForm = urllib.quote_plus(crypto)
	print urlForm
	print newtest

	print rsa.decrypt(urllib.unquote_plus(urlForm),privatekey)
	quickTest = urllib.unquote_plus("%A0%5E%CC_V%17%B9W%E0%D3%93%BF%84%87pqg%07%FA%CC%03%B0%DB%24%99%F7%DCAe%25i%0F-%AC%CA.%B8%2C%E0s%FC%DE%2C%DE%BFF%FA%B0%60%16%D6%92%AE%9DVT%04%83%91%1F%C3%1DI%C0")
	print quickTest
	print rsa.decrypt(quickTest,privatekey)
	print "with utf8"
	#code = urllib.quote(crypto).encode("utf8")
	#code = HttpContext.Current.Server.UrlEncode(urllib.quote_plus(crypto))
	#print rsa.decrypt(urllib.unquote_plus(code),privatekey)
	print rsa.decrypt(urllib.unquote_plus(base64.b64decode(base64.b64encode(urllib.quote_plus(crypto)))),privatekey)

	print base64.b64encode(crypto)

	
