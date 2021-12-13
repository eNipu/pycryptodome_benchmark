from util import *
from Crypto import Random
from Crypto.Cipher import AES
import datetime
import timeit
import io
import os
import zipfile


key = Random.get_random_bytes(AES.block_size)


zip_file_name = 'data.zip'
zip_dir_path = './demo'
zip_a_dir(zip_dir_path, zip_file_name)

zip_file_path = join(zip_dir_path, zip_file_name)
print("*** Encryption Starts *** " + str(datetime.datetime.now()))
start = timeit.default_timer()
cipher = AES.new(key, AES.MODE_GCM)
def encrypt(raw):
    try:
        return cipher.encrypt(raw)
    except(ValueError, KeyError):
        print("Incorrect encryption")


enc_dir_path = './enc'
ciphertext = []
for data in read_large_bin_file(join(enc_dir_path, zip_file_name)):
    ciphertext.append(encrypt(data))

# print(ciphertext)
encrypted_file_name = 'gcm_cipher.bin'
tmp_digest = cipher.digest()
# print(f'nonce= {cipher.nonce}, tag= {cipher.digest()}')

with open(join(enc_dir_path, encrypted_file_name), 'wb') as f:
    for x in (cipher.nonce, cipher.digest(), b"".join(ciphertext)):
        f.write(x)
f.close()

stop = timeit.default_timer()
execution_time = stop - start
print("GCM Encryption executed in: "+str(execution_time))
print("*** Encryption Ends *** " + str(datetime.datetime.now()))


print("*** Decryption Starts *** " + str(datetime.datetime.now()))
start = timeit.default_timer()
file_in = open(join(enc_dir_path, encrypted_file_name), "rb")
nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
# print(f'dec = nonce= {nonce}, tag= {tag}')
cipher = AES.new(key, AES.MODE_GCM, nonce)
result = cipher.decrypt_and_verify(ciphertext, tag)
print(f"IS AUTHENTICATED = {tmp_digest == tag}")

# print(len(ciphertext), type(ciphertext))

with zipfile.ZipFile(io.BytesIO(result), "r") as zf:
    zf.extractall('./dec')

stop = timeit.default_timer()
execution_time = stop - start
print("GCM Decryption executed in: "+str(execution_time))
print("*** Decryption Ends *** " + str(datetime.datetime.now()))

