import csv
import glob
import time
from util import *
from Crypto import Random
from Crypto.Cipher import AES
import datetime
import timeit
import io
import os
import zipfile
import shutil


def delete_files():
    paths = ['./enc/*', './dec/demo/*']
    for p in paths:
        files = glob.glob(p)
        for f in files:
            os.remove(f)


delete_files()


zip_file_name = 'data.zip'
zip_dir_path = './demo'
zip_file_path = join('./enc', zip_file_name)

key = Random.get_random_bytes(AES.block_size)

row_list: list = []
aes_modes = [AES.MODE_GCM, AES.MODE_EAX]
# # aes_modes = [AES.MODE_GCM]
# aes_modes = [AES.MODE_EAX]

for mode in aes_modes:
    rows: list = []
    zip_a_dir(zip_dir_path, zip_file_name)
    zip_file_size = os.path.getsize(zip_file_path)
    zip_file_size = (zip_file_size /(1024*1024))
    print(f"zip_file_size = {zip_file_size}")

    mode_str = None
    if mode == AES.MODE_GCM:
        mode_str = "AES_GCM"
    elif mode == AES.MODE_EAX:
        mode_str = "AES_EAX"
    elif mode == AES.MODE_CCM:
        mode_str = "AES_CCM"

    rows.append(mode_str)
    rows.append(zip_file_size)

    print("*** Encryption Starts *** " + str(datetime.datetime.now()))
    start = timeit.default_timer()

    cipher = None
    if mode == AES.MODE_GCM or mode == AES.MODE_EAX:
        cipher = AES.new(key, mode)
    elif mode == AES.MODE_CCM:
        cipher = AES.new(key, mode, msg_len=8)
    else:
        print('MODE NOT FOUND')
    # def encrypt(raw):
    #     try:
    #         return cipher.encrypt(raw)
    #     except(ValueError, KeyError):
    #         print("Incorrect encryption")

    enc_dir_path = './enc'
    ciphertext = []
    enc_file = join(enc_dir_path, zip_file_name)
    if mode == AES.MODE_GCM or mode == AES.MODE_EAX:
        for data in read_large_bin_file(enc_file, 1024):
            ciphertext.append(cipher.encrypt(data))
    elif mode == AES.MODE_CCM:
        for data in read_large_bin_file(enc_file, 8):
            print(len(data))
            ciphertext.append(cipher.update(data))

    # print(ciphertext)
    encrypted_file_name = 'cipher.bin'
    tmp_digest = cipher.digest()
    enc_file_path = join(enc_dir_path, encrypted_file_name)
    # print(f'nonce= {cipher.nonce}, tag= {cipher.digest()}')

    with open(enc_file_path, 'wb') as f:
        for x in (cipher.nonce, cipher.digest(), b"".join(ciphertext)):
            f.write(x)
    f.close()

    stop = timeit.default_timer()
    enc_execution_time = stop - start
    print(f"{mode_str} Encryption executed in: "+str(enc_execution_time))
    print("*** Encryption Ends *** " + str(datetime.datetime.now()))

    # ciphertext.clear()


    #----------------------------------------------DEC--------------------------
    print("*** Decryption Starts *** " + str(datetime.datetime.now()))
    start = timeit.default_timer()

    file_in = open(join(enc_dir_path, encrypted_file_name), "rb")
    nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
    # print(f'dec = nonce= {nonce}, tag= {tag}')

    cipher = AES.new(key, mode, nonce)
    result = cipher.decrypt_and_verify(ciphertext, tag)

    print(f"IS AUTHENTICATED = {tmp_digest == tag}")
    print(len(ciphertext), type(ciphertext), len(result))


    with zipfile.ZipFile(io.BytesIO(result), "r") as zf:
        zf.extractall('./dec')

    stop = timeit.default_timer()
    execution_time = stop - start
    print("GCM Decryption executed in: "+str(execution_time))
    print("*** Decryption Ends *** " + str(datetime.datetime.now()))
    enc_file_size = os.path.getsize(enc_file_path)
    print(f"enc_file_size = {enc_file_size}")
    enc_file_size = (enc_file_size / (1024*1024))
    rows.append(enc_file_size)
    rows.append(enc_execution_time)
    rows.append(execution_time)
    row_list.append(rows)
    if os.path.exists("./enc/data.zip"):
        os.remove("./enc/data.zip")
        os.remove("./enc/cipher.bin")
        shutil.rmtree("./dec/demo")
        # shutil.rmtree("./enc")
    else:
        print("The file does not exist")
    # time.sleep(20)


print(row_list)
with open('result.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(
        ['AES_MODE', 'Zip_Size (MB)', 'Encrypted Bin Size (MB)', 'ENC Time', 'DEC_TIME'])
    writer.writerows(row_list)
