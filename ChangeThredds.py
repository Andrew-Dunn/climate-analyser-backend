import rsa
import zoo

def ChangeThredds(conf,inputs,outputs):
	crypto = inputs["url"]["value"]
	
	privatefile = open('rsa/privateKey.pem')
	keydata = privatefile.read()
	privatekey = rsa.PrivateKey.load_pkcs1(keydata)
	publicfile = open('rsa/publicKey.pem')
	pubdata = publicfile.read()
	pubkey = rsa.PublicKey.load_pkcs1(pubdata)
	
	newurl = rsa.decrypt(crypto,privatekey)

	ThreddServer = open('ThreddServer','w')
	ThreddServer.write(newurl)

        outputs["Result"]["value"]=("New Server address is " + newurl)

	return zoo.SERVICE_SUCCEEDED
