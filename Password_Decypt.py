from hashlib import md5
from multiprocessing import pool
import re
import binascii
import itertools
import time
import multiprocessing
import os
def Strip(shadow):
    magic = re.search(r"(\$).\W",shadow)
    salt = re.search(r"([^(\x24)1(\x24).]+\S\b\x24)",shadow)
    output = re.search(r"([(\x24).+:/.][a-zA-Z]\S+)[.]",shadow)
    return magic.group(),salt.group()[:-1],output.group()[1:]

def Password_Gen(password,salt,magic):
   
        
    #TEST REWRITING PASSWORD 
    # password = 'zhgnnd'
    #  # password = ' oyjivl'
    # salt = "hfT7jp2q"
        
    # 2.START BY COMPUTING THE ALT SUM
    alt_concatenation = Alt_Sum(password,salt).digest()
    # print('alt_concatenation',alt_concatenation)


    # 3.COMPUTE THE INTERMEDIATE_0 SUM BY HASHING CONCATENATION
    concatenation = Intermediate(password, magic, salt, alt_concatenation).digest()
    # print(concatenation)


    # 4.INTERMEDIATE LOOP 
    loop_concatenation = Intermediate_Loop(concatenation,password,salt)
        

    # 5.CRYOT BASE 64
    final_hash = Cryot_Base(loop_concatenation)
    return final_hash
    # print(final_hash)

def Alt_Sum(password,salt):
    hash_string = password + salt + password
    return md5(hash_string.encode())

def Cryot_Base(loop_concatenation):
    crypt_bas64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    Final_hash = ''
    # Reordered Loop Concatenation
    ordered_bits = [11, 4, 10, 5, 3, 9, 15, 2, 8, 14, 1, 7, 13, 0, 6, 12]

    arr_hex = Space(loop_concatenation.hex(),2)

    ordered_string = b''
    for i in ordered_bits:
        ordered_string += arr_hex[i].encode()
    
    bytes_string = binascii.unhexlify( ordered_string)
    int_bytes = int.from_bytes(bytes_string,'big')
    
    for i in range(22):
        index = int_bytes%64
        Final_hash += crypt_bas64[index]
        
        # floor divison 
        int_bytes //= 64
    return Final_hash

def Space(string_hex,n):
   
    space_hex = []
    for i in range(0,len(string_hex),n):
        part = string_hex[i:i+n]
        space_hex.append(part)
        
    return space_hex

def Intermediate(password, magic, salt, alt_concatenation):

    len_of_password = len(password)
    # CONCATENATION OF PASSWORD + MAGIC + SALT
    concatenation = password + magic + salt 
    
   

    # CUT 6 BIT LENGTH FROM ALT_CONCATENATION
    hex_str = alt_concatenation[:len_of_password]
  
    # ADDING CUT LEN
    concatenation = bytes(concatenation,'utf-8')
    concatenation += hex_str
    
    # APPENDING SET BITS. SINCE LEN = 6(110), 1 == NULL BYTE , null == FIRST BYTE OF PASSWORD 
    set_bit = format(len_of_password,'b')
  
    for i in reversed(set_bit):
        if i == '0':
            concatenation += bytes(password[0],'utf-8')
        else:
            concatenation += bytes('\0','utf-8')

    return md5(concatenation)

def Intermediate_Loop(concatenation,password,salt):

    for i in range(1000):
        inter = bytes('','utf-8')
        if i % 2 == 0:
            inter += concatenation
        else:
            inter += bytes(password,'utf-8')
            
        if i % 3 != 0:
            
            inter += bytes(salt,'utf-8')
            
        if i % 7 != 0:
            
            inter += bytes(password,'utf-8')
            
        if i % 2 == 0:
            
            inter += bytes(password,'utf-8')
            
        else:
            inter += concatenation
        concatenation = md5(inter).digest()
    # print(concatenation.hex())
    
    return concatenation
    


alpha_set = 'abcdefghijklmnopqrstuvwxyz'
print(len(alpha_set))
num_parts = 6
part_size = len(alpha_set)//num_parts



def Do_Work(first_bits):
    print('process id:', os.getpid())
    file = open('etc_shadow')
    content = file.readlines()
    shadow = content[22]
    magic,salt,encrypted = Strip(shadow)
    'THIS IS ITER '
    for x in itertools.product(first_bits,alpha_set,alpha_set,alpha_set,alpha_set,alpha_set):
        password = ''.join(x)
        # print(password)
        Final_hash = Password_Gen(password,salt,magic)
        if Final_hash == encrypted:
            print("PASSWORD: ",password)
            return password
    print('finished',first_bits)
    

        
        
if __name__ == "__main__":


    "THE NUMBER OF CPU THREADS"
    pool = multiprocessing.Pool(processes=6)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    print('part_size',part_size)
    password = ''
    t1 = time.time()
    print('START TIME',t1)
    for i in range(num_parts):
        # print('process id:', os.getpid())
        if i == num_parts-1:
            first_bit = alpha_set[part_size*i: ]
            print(first_bit)
        else:
            first_bit = alpha_set[part_size*i:part_size*(i+1)]
            print('else',first_bit)
        # Do_Work(first_bit)
        # pool.map(Do_Work,first_bit)
        password = pool.starmap(Do_Work,first_bit)
        if password != '':
            i = 6
        # pool.close()
        # pool.join()
        # if check == 1:
        #     pool.terminate()
        #     pool.join()
    print(password)
    pool.close()
    pool.join()
    print("END TIME:", time.time() - t1)

    
'Answers Regarding The Project '
'Show the correct password for your team user.'
# PASSWORD:  xqcqct

' The number of threads/processes is used.'
# The program ran using four threads although six threads were assigned 

'The CPU model that your code is run on'
# Apple M1 Silicon 

'The throughput of password cracking,'
# Although I was using multiple threads. 
# The way I implemented the iteration of the permutations resulted in poor run time.
#  My program was running finishing 4 iterations in 7 hours. 



