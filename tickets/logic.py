from web3 import Web3
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

    # Obtenemos la contraseña del usuario que va a mandar la transaccion
    with open("pass") as f:
        fil = f.read()
        privateKey = w3.eth.account.decrypt(fil, '1234')

    # Preparamos la transaccion
    nonce = w3.eth.getTransactionCount(w3.toChecksumAddress("0x1e264979ee1de3aa23e9c57f3c4d2e8dd4142549"))
    params = {'accessKey': accessKey, 'data': "PAULA POUSA",
              'address': w3.toChecksumAddress("0x1e264979ee1de3aa23e9c57f3c4d2e8dd4142549"), 'nonce': nonce}
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
    print(res)


def signTransaction(tx):
    signed = w3.eth.account.sign_transaction(tx, private_key=privateKey)
    return signed
