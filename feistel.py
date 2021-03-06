#!/usr/bin/python3.5
#
# =====================================================================================
#
#       Filename:  otp.py
#
#    Description: Build a Feistel network using ECB
#
#        Created:  03/04/2019
#
#         Author:  Benedict Lo & Aing Ragunathan
#
# =====================================================================================

import sys, argparse

#
# =====================================================================================
#
#       Function:  function()
#
#     Parameters: i - iterations
#                 k - key
#                 length - length of key
#
#    Description: complete function
#
#        Created:  03/04/2019
#
#         Author:  Benedict Lo & Aing Ragunathan
#
# =====================================================================================


def function(i, k, r, length):
    #print("xoring: ", ((2*i*r)**k) % (10**(length+1)))
    return ((2*i*r)**k) % (10**(length))

#
# =====================================================================================
#
#       Function:  main()
#
#        Created:  03/04/2019
#
#         Author:  Benedict Lo & Aing Ragunathan
#
# =====================================================================================

def main(argv):
    l0 = 0
    r0 = 0
    l_old = 0
    r_old = 0
    l_new = 0
    r_new = 0
    k = 7
    iterations = 9

    plaintext = ''
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', action="store",dest="filename")
    parser.add_argument('-m', action="store",dest="message")

    if parser.parse_args().filename:
        filename = str(parser.parse_args().filename)
        file = open(filename)
        plaintext = file.read()
    elif parser.parse_args().message:
        file = open('input.txt', 'w+')
        file.write(parser.parse_args().message)
        file = open('input.txt', 'r')
        plaintext = file.read()

    if len(plaintext) % 2 != 0:
        plaintext += ' '

    l0_string = plaintext[:int(len(plaintext)/2)]
    r0_string = plaintext[int(len(plaintext)/2):]

    l0 = int.from_bytes(l0_string.encode('utf-8'), byteorder='big')
    r0 = int.from_bytes(r0_string.encode('utf-8'), byteorder='big')

    print("number of digits:", len(str(abs(l0))))
    length = len(str(abs(l0)))

    print("plaintext")
    print("l_plain = ", l0_string)
    print("r_plain = ", r0_string)
    #print("l_inverse = ", int.to_bytes(l0, length=len(l0_string), byteorder='big').decode('utf-8'))
    #print("r_inverse = ", int.to_bytes(r0, length=len(r0_string), byteorder='big').decode('utf-8'))
    print("l_plain_int:", l0)
    print("r_plain_int:", r0)
    print()

    l_old = l0
    r_old = r0

    #encrypt
    for i in range(1, iterations):
        l_new = r_old
        #r_new = xor(f(r_old, k), l)
        #r_new = (((2*i*k)*r_old) % 15) ^ l_old
        print("xoring: ", function(i, k, r_old, length), "^", l_old)
        r_new = function(i, k, r_old, length) ^ l_old

        #update nanmes for next iteration
        l_old = l_new
        r_old = r_new

        print("ciphertext")
        '''
        print("l_cipher = ", int.to_bytes(l_new, length=len(l0_string), byteorder='big').decode('utf-8'))
        print("r_cipher = ", int.to_bytes(r_new, length=len(r0_string), byteorder='big').decode('utf-8'))
        '''
        print("l new:", l_new)
        print("r new:", r_new)
        print()

    #decrypt
    for i in range(iterations-1, 0, -1):
        r_new = l_old
        print("xoring: ", function(i, k, r_new, length), "^", r_old)
        l_new = function(i, k, r_new, length) ^ r_old
        l_old = l_new
        r_old = r_new

        print("decrypted")
        '''
        print("l_decrypted = ", int.to_bytes(l_new, length=len(l0_string), byteorder='big').decode('utf-8'))
        print("r_decrypted = ", int.to_bytes(r_new, length=len(r0_string), byteorder='big').decode('utf-8'))
        '''
        print("l new:", l_new)
        print("r new:", r_new)
        print()

if __name__ == "__main__":
    main (sys.argv[1:])
