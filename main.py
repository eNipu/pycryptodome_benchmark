from aes_cbc import *
from aes_ecb import *
from aes_ctr import *
from aes_ofb import *
from aes_opengpg import *
from aes_gcm import *
from aes_siv import *
import aes_mode_const as mode
from Crypto.Random import get_random_bytes
import timeit
from binascii import unhexlify
import time


def bench_gcm(key, message):
    #---------------------GCM BENCH MARK---------------------
    print(f"--------------------GCM BENCH MARK STARTS-------------------\n")
    aes_pgp_cipher = AesGcm(key)
    start = timeit.default_timer()
    encrypted = aes_pgp_cipher.encrypt(message)
    encrypted2 = aes_pgp_cipher.encrypt(message)
    print(f"Deterministic = {encrypted==encrypted2}")
    stop = timeit.default_timer()
    execution_time = stop - start
    print("GCM Encryption executed in: "+str(execution_time))

    # print(encrypted)
    start = timeit.default_timer()
    decrypted = aes_pgp_cipher.decrypt(encrypted)
    # print(decrypted)
    stop = timeit.default_timer()
    execution_time = stop - start
    print("GCM decryption executed in: "+str(execution_time))
    print(f"MES = DEC(ENC(MES)) = {message == decrypted}")

    print(f"\n--------------------GCM BENCH MARK ENDS-------------------\n")
    #---------------------GCM BENCH MARK---------------------


def bench_ofb(key, message):
    #---------------------OFB BENCH MARK---------------------
    print(f"--------------------OFB BENCH MARK STARTS-------------------\n")
    aes_pgp_cipher = AesOfb(key)
    start = timeit.default_timer()
    encrypted = aes_pgp_cipher.encrypt(message)
    stop = timeit.default_timer()
    execution_time = stop - start
    print("OFB Encryption executed in: "+str(execution_time))

    # print(encrypted)
    start = timeit.default_timer()
    decrypted = aes_pgp_cipher.decrypt(encrypted)
    # print(decrypted)
    stop = timeit.default_timer()
    execution_time = stop - start
    print("OFB decryption executed in: "+str(execution_time))
    print(f"MES = DEC(ENC(MES)) = {message == decrypted}")

    print(f"\n--------------------OFB BENCH MARK ENDS-------------------\n")
    #---------------------OFB BENCH MARK---------------------

def bench_openpgp(key, message):
    #---------------------OPENPGP BENCH MARK---------------------
    print(f"--------------------OPENPGP BENCH MARK STARTS-------------------\n")
    # aes_pgp_cipher = AesOpenPgp(key)
    aes_pgp_cipher = AesOfb(key)
    start = timeit.default_timer()
    encrypted = aes_pgp_cipher.encrypt(message)
    stop = timeit.default_timer()
    execution_time = stop - start
    print("OPENPGP Encryption executed in: "+str(execution_time))

    # print(encrypted)
    start = timeit.default_timer()
    decrypted = aes_pgp_cipher.decrypt(encrypted)
    # print(decrypted)
    stop = timeit.default_timer()
    execution_time = stop - start
    print("OPENPGP decryption executed in: "+str(execution_time))
    print(f"MES = DEC(ENC(MES)) = {message == decrypted}")

    print(f"\n--------------------OPENPGP BENCH MARK ENDS-------------------\n")
    #---------------------OPENPGP BENCH MARK---------------------



def bench_ctr(key, message):
    #---------------------CTR BENCH MARK---------------------
    print(f"---------------------CTR BENCH MARK STARTS---------------------\n")
    aes_ctr_cipher = AesCtr(key)
    start = timeit.default_timer()
    encrypted = aes_ctr_cipher.encrypt(message)
    stop = timeit.default_timer()
    execution_time = stop - start
    print("CTR Encryption executed in: "+str(execution_time))

    # print(encrypted)
    start = timeit.default_timer()
    decrypted = aes_ctr_cipher.decrypt(encrypted)
    # print(decrypted)
    stop = timeit.default_timer()
    execution_time = stop - start
    print("CTR decryption executed in: "+str(execution_time))
    print(f"MES = DEC(ENC(MES)) = {message == decrypted}")

    print(f"\n---------------------CTR BENCH MARK ENDS---------------------\n")
    #---------------------CTR BENCH MARK---------------------


def bench_ecb(key, message):
    #---------------------ECB BENCH MARK---------------------
    print(f"---------------------ECB BENCH MARK STARTS---------------------\n")
    aes_ecb_cipher = AesEcb(key)
    start = timeit.default_timer()
    encrypted = aes_ecb_cipher.encrypt(message)
    stop = timeit.default_timer()
    execution_time = stop - start
    print("ECB Encryption executed in: "+str(execution_time))

    # print(encrypted)
    start = timeit.default_timer()
    decrypted = aes_ecb_cipher.decrypt(encrypted)
    # print(decrypted)
    stop = timeit.default_timer()
    execution_time = stop - start
    print("ECB decryption executed in: "+str(execution_time))
    print(f"MES = DEC(ENC(MES)) = {message == decrypted}")

    print(f"\n---------------------ECB BENCH MARK ENDS---------------------\n")
    #---------------------ECB BENCH MARK---------------------

def bench_cbc(key, message):
    #---------------------CBC BENCH MARK---------------------
    print(f"---------------------CBC BENCH MARK STARTS---------------------\n")
    aes_cbc_cipher = AesCbc(key)
    start = timeit.default_timer()
    encrypted = aes_cbc_cipher.encrypt(message)
    stop = timeit.default_timer()
    execution_time = stop - start
    print("CBC Encryption executed in: "+str(execution_time))

    # print(encrypted)
    start = timeit.default_timer()
    decrypted = aes_cbc_cipher.decrypt(encrypted)
    # print(decrypted)
    stop = timeit.default_timer()
    execution_time = stop - start
    print("CBC decryption executed in: "+str(execution_time))
    print(f"MES = DEC(ENC(MES)) = {message == decrypted}")
    print(f"\n---------------------CBC BENCH MARK ENDS---------------------\n")
    #---------------------CBC BENCH MARK---------------------


if __name__ == '__main__':
    key = get_random_bytes(AES.block_size)
    message = "A SIMPLE STRING"
    # bench_cbc(key, message)
    # bench_ecb(key, message)
    # bench_ctr(key, message)
    # bench_openpgp(key, message)
    # bench_ofb(key, message)
    # bench_gcm(key, message)
    # zip_a_dir('./demo', 'data.zip')


