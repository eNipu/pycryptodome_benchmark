import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Padding


class AesCbc(object):
    def __init__(self, key):
        self.key = (hashlib.md5(key).hexdigest()).encode('utf-8')
        print(self.key)

    def encrypt(self, raw):
        iv = Random.get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        data = Padding.pad(raw.encode('utf-8'), AES.block_size, 'pkcs7')
        return base64.b64encode(iv + cipher.encrypt(data))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        print(f"")
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        data = Padding.unpad(cipher.decrypt(
            enc[AES.block_size:]), AES.block_size, 'pkcs7')
        return data.decode('utf-8')
