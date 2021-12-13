import base64
import json
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes
from Crypto.Util import Padding


class AesSiv(object):
    def __init__(self, key):
        key = Random.get_random_bytes(16 * 2)
        self.key = (hashlib.md5(key).hexdigest()).encode('utf-8')
        self.mode = AES.MODE_SIV
        print(self.key)

    def encrypt(self, raw):
        ret: dict = {}
        try:
            nonce = Random.get_random_bytes(AES.block_size)
            header = b"header"
            cipher = AES.new(self.key, self.mode)
            cipher.update(header)
            ciphertext, tag = cipher.encrypt_and_digest(raw.encode('utf-8'))
            # print(type(tag))
            json_k = ['header', 'ciphertext', 'tag']
            json_v = [base64.b64encode(x).decode('utf-8')
                      for x in [header, ciphertext, tag]]
            result = json.dumps(dict(zip(json_k, json_v)))
            print(result)
            ret = result
            return ret
        except(ValueError, KeyError):
            print("Incorrect encryption")

    def decrypt(self, json_input):
        try:
            b64 = json.loads(json_input)
            json_k = ['header', 'ciphertext', 'tag']
            jv = {k: base64.b64decode(b64[k]) for k in json_k}

            cipher = AES.new(self.key, self.mode)
            cipher.update(jv['header'])
            plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
            print("The message was: " + plaintext.decode('utf-8'))
            return plaintext.decode('utf-8')
        except (ValueError, KeyError):
            print("Incorrect decryption")
