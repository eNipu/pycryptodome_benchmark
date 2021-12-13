from subprocess import Popen, PIPE, call
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from io import StringIO, BytesIO
import io
import tarfile
import os
import sys
import datetime
import timeit

file_name = "out.tar.gz"

print("*** Compressing starts ***")

cmd = [f"tar -zcvf {file_name} demo"]
call(cmd, shell=True)

print ("*** Encryption Starts *** " + str(datetime.datetime.now()))
key = get_random_bytes(32)


def readLargeFile(filename):
    with open(filename, "rb") as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            yield data


# cmd = ["tar --acls --selinux -czPf out.tar.gz ./encrypt_disk/src/*"]
# cmd = ["tar --acls -czPf out.tar.gz ./encrypt_disk/src/*"]
# call(cmd, shell=True)

cipher = AES.new(key, AES.MODE_GCM)
ciphertext = []

for data in readLargeFile("out.tar.gz"):
    ciphertext.append(cipher.encrypt(data))

out = open("out.bin", "wb")
[out.write(x) for x in (cipher.nonce, cipher.digest(), b"".join(ciphertext))]
out.close()
print ("*** Encryption Ends *** " + str(datetime.datetime.now()))


print ("*** Decryption Starts *** " + str(datetime.datetime.now()))
file_in = open("out.bin", "rb")
nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
cipher = AES.new(key, AES.MODE_GCM, nonce)
result = cipher.decrypt_and_verify(ciphertext, tag)
print(len(result))



file_like_object = io.BytesIO(result)
print(type(file_like_object))
tar = tarfile.open(fileobj=file_like_object, mode='r|*')
# use "tar" as a regular TarFile object
for member in tar.getmembers():
    f = tar.extractfile(member)
    print(f)
# tar = tarfile.open(fileobj=result)
# os.chdir("dst")
# tar.extractall(path='.')
print ("*** Decryption Ends *** " + str(datetime.datetime.now()))


# os.remove("./enc/data.zip")
