from web3 import Web3,HTTPProvider
from hexbytes import HexBytes
import requests, json

w3 = Web3(Web3.HTTPProvider("http://138.100.10.126:22000"))

# Clase que permite convertir un diccionario en JSON
class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)

def sendData(accessKey):
    
    # Preparamos la transaccion
    nonce = w3.eth.getTransactionCount(w3.toChecksumAddress("0xa832ac7b2e2e5bf8809dac391cd7a8076877b85b"))
    params = {'accessKey': accessKey, 'address':w3.toChecksumAddress("0xa832ac7b2e2e5bf8809dac391cd7a8076877b85b"), 'nonce':nonce}
    res = requests.post('http://138.100.10.226:4040/prepareTx', data=params)
    tx = json.loads(res.text)
    
    # Firmamos la transaccion
    signed = signTransaction(tx)
    
    # Lo convertimos en JSON
    tx_dic = dict(signed)
    tx_json = json.dumps(tx_dic, cls=HexJsonEncoder)
    
    # Mandamos la transaccion
    params = {'data': tx_json}
    res = requests.post('http://138.100.10.226:4040/registerAssistance', data=params)
    res = res.text

def signTransaction(tx):
    
    # Obtenemos la contraseña del usuario que va a mandar la transaccion
    with open(".password.json") as ff:
        d = json.load(ff)
        password = d["password"]
    
    with open(".pass") as f:
        fil = f.read()
        privateKey = w3.eth.account.decrypt(fil, password)
    
    signed = w3.eth.account.signTransaction(tx, private_key=privateKey)
    return signed
