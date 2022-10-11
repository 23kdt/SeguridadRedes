
import string

encrypted_message = input("Introduce el texto: ")
key = 26 -(int(input("Introduce la clave: ")))   #número de rotaciones del cifrado cesar. 


encrypted_message = encrypted_message.replace('OK','')
encrypted_message = encrypted_message.replace('..','')
plaintext = encrypted_message.lower()


def cesar(plaintext, key):
    ciphertext = ""
    for c in plaintext:
        if c in string.printable:
            temp = ord(c) + key

            if temp > ord('z'):
                temp = temp - 26

            ciphertext = ciphertext + chr(temp)
        else:
            ciphertext = ciphertext + c
        

    
    ciphertext = ciphertext.replace(':',' ')

    return ciphertext

print(cesar(plaintext,key))
