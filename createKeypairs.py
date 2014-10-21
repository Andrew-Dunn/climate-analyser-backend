import rsa

def createKeyPairs():
	(pub,private) = rsa.newkeys(512)
	ppub = open("publicKey.pem",'w')
	ppub.write(pub.save_pkcs1())
	ppub.close()

	ppriv = open("privateKey.pem",'w')
	ppriv.write(private.save_pkcs1())
	ppriv.close()

if __name__ == '__main__':
    createKeyPairs()
