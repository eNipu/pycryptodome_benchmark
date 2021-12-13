import base64
import json
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Padding


class AesCtr(object):
    def __init__(self, key):
        self.key = (hashlib.md5(key).hexdigest()).encode('utf-8')
        self.mode = AES.MODE_CTR
        print(self.key)

    def encrypt(self, raw):
        ret: dict = {}
        try: 
            cipher = AES.new(self.key, self.mode)
            ct_bytes = cipher.encrypt(raw.encode('utf-8'))
            nonce = base64.b64encode(cipher.nonce).decode('utf-8')
            ct = base64.b64encode(ct_bytes).decode('utf-8')
            ret = json.dumps({'nonce': nonce, 'ciphertext': ct})
            print(ret)
            return ret
        except(ValueError, KeyError):
            print("Incorrect encryption")

    def decrypt(self, json_input):
        try:
            b64 = json.loads(json_input)
            nonce = base64.b64decode(b64['nonce'])
            ct = base64.b64decode(b64['ciphertext'])
            cipher = AES.new(self.key, self.mode, nonce=nonce)
            data = cipher.decrypt(ct)
            return data.decode('utf-8')
        except(ValueError, KeyError):
            print("Incorrect decryption")
