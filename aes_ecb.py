import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Padding


class AesEcb(object):
    def __init__(self, key):
        self.key = (hashlib.md5(key).hexdigest()).encode('utf-8')
        self.mode = AES.MODE_ECB
        # print(self.key)

    def encrypt(self, raw):
        cipher = AES.new(self.key, self.mode)
        data = Padding.pad(raw.encode('utf-8'), AES.block_size, 'pkcs7')
        return base64.b64encode(cipher.encrypt(data))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, self.mode)
        data = Padding.unpad(cipher.decrypt(enc), AES.block_size, 'pkcs7')
        return data.decode('utf-8')
