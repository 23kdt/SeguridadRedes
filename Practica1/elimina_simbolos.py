from pydoc import plain
import string

plaintext = input("Introduce el texto: ")

def eliminar(plaintext):

    clean_text = plaintext.replace('OK','')

    return clean_text



print('\n\n\n'+eliminar(plaintext))