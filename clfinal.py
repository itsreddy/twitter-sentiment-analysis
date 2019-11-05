import os
import socket
import thread
import shutil
from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
s = socket.socket()
host = "192.168.43.192"
port = 9000
s.connect((host, port)) #Connect host to server socket to specfied ip and port
path = "."
directory = os.listdir(path)


def derive_key_and_iv(password, salt, key_length, iv_length): #Derives the key
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]


def encrypt(in_file, out_file, password, key_length=32): #Encryption
    bs = AES.block_size
    salt = Random.new().read(bs - len('Salted__'))
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write('Salted__' + salt)
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = bs - (len(chunk) % bs)
            chunk += padding_length * chr(padding_length)
            finished = True
        out_file.write(cipher.encrypt(chunk))

def decrypt(in_file, out_file, password, key_length=32): #Decryption
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            if padding_length < 1 or padding_length > bs:
               raise ValueError("bad decrypt pad (%d)" % padding_length)
            # all the pad-bytes must be the same
            if chunk[-padding_length:] != (padding_length * chr(padding_length)):
               # this is similar to the bad decrypt:evp_enc.c from openssl program
               raise ValueError("bad decrypt") 
            chunk = chunk[:-padding_length]
            finished = True
        out_file.write(chunk)


#----------------------------------Device type information----------------------------------

device_type="1"
print 'device type sent'
size = len(device_type)#Gets the size of the Device Type being used
size = bin(size)[2:].zfill(16) # encode filename size as 16 bit binary
s.send(size) #Transfer the size bits on the socket
#s.send(filename)
s.send(device_type)#Transfer the device name of length=size on the socket


#-------------------------------------Compression-------------------------------------------
shutil.make_archive('Pupil','zip','/home/rushin/Hippo\ Campus/dece')

#-------------------------------------Encryption--------------------------------------------

encrypted_file_name="Pupil_enc"
with open('/home/rushin/Hippo\ Campus/Pupil.zip','rb') as in_file , open(encrypted_file_name,'wb') as out_file:# encrypted_file_name is the name of the encrypted file that will be created
     encrypt(in_file,out_file,"qwerty")#qwerty is the password


#-------------------------------Transfer of Encrypted File----------------------------------- 

size_enc=len(encrypted_file_name)#length of the encrypted_file_name
size=bin(size_enc)[2:].zfill(16)
s.send(size)#sending the length of the name in binary on the socket
s.send(encrypted_file_name)#Sending the encrypted file name of length=size on the socket at 4KB per stream

filepath=os.path.abspath(encrypted_file_name)#get the path of the File on the system
filesize=os.path.getsize(filepath)#stores the size of the FILE. The function doesn't mean it stores the size of the "file path". 
print filesize
filesize= bin(filesize)[2:].zfill(32)#Convert the size of file to binary
s.send(filesize)#Send the size of the Main File to be Transferred
print filesize
file_to_send=open(encrypted_file_name,"rb")
l=file_to_send.read()#Basic reading of bytes to be sent on the socket
s.sendall(l)#Send the bytes read above on the socket
file_to_send.close()


print "Encrypted File sent"
s.close()
