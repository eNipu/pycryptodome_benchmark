import base64
import json
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Padding
import traceback


class AesOpenPgp(object):
    def __init__(self, key):
        self.key = (hashlib.md5(key).hexdigest()).encode('utf-8')
        self.mode = AES.MODE_OPENPGP
        print(self.key)

    def encrypt(self, raw):
        ret: dict = {}
        try:
            iv = Random.get_random_bytes(AES.block_size)
            cipher = AES.new(self.key, self.mode, iv)
            ct_bytes = cipher.encrypt(raw.encode('utf-8'))
            ret  = base64.b64encode(ct_bytes)
            return ret
        except(ValueError, KeyError):
            print("Incorrect encryption")

    def decrypt(self, input):
        try:
            enc = base64.b64decode(input)
            eiv_size = AES.block_size + 2
            eiv = enc[:eiv_size]
            ct = enc[eiv_size:]
            cipher = AES.new(self.key, self.mode, eiv)
            data = cipher.decrypt(ct)
            ret = data.decode('utf-8')
            # print(ret)
            return ret
        except Exception as exception:
            print("Incorrect decryption")
            traceback.print_exc()
