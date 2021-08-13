from time import sleep
import os
import sys
from threading import Thread

archive_path = './STORAGE'
separator = "||__||"

class File():

    default = "Write not specified"

    def __init__(self,file = f"{__name__}.py"):
        self.file = file

    def read(self):
        with open(self.file,"r") as file:
            return file.read()

    def read_bytes(self):
        with open(self.file,"rb") as file:
            return file.read()

    def write_bytes(self,content):
        with open(self.file,"wb") as file:
            file.write(content)

    def append_bytes(self,content):
        with open(self.file,"ab") as file:
            file.write(content)

    def overwrite(self,content = default):
        with open(self.file,"w") as file:
            file.write(content)

    def write(self,content = default):
        self.overwrite(content)

    def append(self,content = default):
        with open(self.file,"a") as file:
            file.write(content)

    def char_count(self):
        return len(self.read())

    def word_count(self):
        return len(self.read().split())

    def readlines(self):
        return self.read().split("\n")

    def readline(self,n:int):
        i = 0
        for line in self.readlines():
            i += 1
            if i == n:
                return line
        return None

    def find(self,search:str="None",case_sensitive:bool=False,whole_line:bool=False):
        list = []
        n = 0
        failed = True
        if not case_sensitive:
            _search = search.lower()
        else:
            _search = search
        for line in self.readlines():
            c = 0
            n += 1
            i = 0
            if not case_sensitive:
                _line = line.lower()
            else:
                _line = line
            if _search in _line:
                if whole_line:
                    list.append(line)
                else:
                    for char in _line:
                        c += 1
                        if not failed and i == len(search):
                            list.append(f"Line {n}, column {c - i}")
                            i = 0
                            failed = True
                        else:
                            if char[0] == _search[i]:
                                failed = False
                                i += 1
                            else:
                                i = 0
                                failed = True

        return list

def encrypt(key, bytes_list):
    encoded_items = []
    bytes_list = [b'%c' % i for i in bytes_list]
    for i in range(len(bytes_list)):
        key_c = key[i % len(key)]
        encoded_c = (int.from_bytes(bytes_list[i], sys.byteorder) + ord(key_c)) % 512
        encoded_items.append(str(encoded_c) + separator)
    return encoded_items

def decrypt(key, bytes_list):
    encoded_items = []
    temp = bytes_list.split(separator)
    bytes_list = []
    for i in temp:
        try:
            bytes_list.append(int(i))
        except:
            pass
    for i in range(len(bytes_list)):
        key_c = key[i % len(key)]
        encoded_c = (bytes_list[i] - ord(key_c) + 512) % 512
        encoded_items.append(encoded_c.to_bytes(1, sys.byteorder))
    return encoded_items

def unlock(key:str):
    global processing
    processing = True
    print("Encoding passkey...")
    sleep(0.1)
    print("Getting file data...")
    files = [f for f in os.listdir(archive_path) if os.path.isfile(os.path.join(archive_path, f))]
    sleep(0.1)
    try: files.remove('.DS_Store')
    except: pass
    files_n = len(files)
    count = 0
    sleep(0.1)
    for item in files:
        count += 1
        print(f"Rewriting files... {count}/{files_n}")

        file = File(f"{archive_path}/{item}")

        try:
            data_buffer = file.read()
            if not "_*" in data_buffer:
                continue
        except:
            continue

        try:
            decrypted = decrypt(key, data_buffer.lstrip("_*"))
            file.write_bytes(b''.join(decrypted))
        except:
            print(f"Error on file {count}/{files_n}\nFile name: {item}")
            sleep(1)
            sleep(0.1)
            processing = False
            return

        sleep(0.1)
    print(f"Successfully decrypted files!")
    processing = False

def lock(key:str):
    global processing
    processing = True
    print("Encoding passkey...")
    sleep(0.1)
    print("Getting file data...")
    files = [f for f in os.listdir(archive_path) if os.path.isfile(os.path.join(archive_path, f))]
    sleep(0.1)
    try: files.remove('.DS_Store')
    except: pass
    files_n = len(files)
    count = 0
    sleep(0.1)
    locked = True
    for file in files:
        count += 1
        print(f"Rewriting files... {count}/{files_n}")
        print(file)

        file_obj = File(f"{archive_path}/{file}")

        data_buffer = file_obj.read_bytes()
        try:
            if "_*" in file_obj.read():
                continue
        except:
            pass

        try:
            encrypted = encrypt(key, data_buffer)
            file_obj.overwrite("_*" + ''.join(encrypted))
            locked = False
        except Exception as e:
            print(f"Error on file {count}/{files_n}\nFile: {file}")
            print(e)
            sleep(1)
            processing = False
            return

        sleep(0.1)
    print(f"Successfully encrypted files!")
    processing = False
    
processing = False
passkey = input("Input password: ")
choice = input("Lock/Unlock: ").lower()
if choice.startswith("lock"):
	lock(passkey)
else:
	unlock(passkey)
