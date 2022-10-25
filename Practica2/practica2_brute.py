#####################################
#
#   Autor: Diego Dorado Galán
#
#   Nombre: practica2_brute.py
#   
#####################################


import os
import sys
import time
import string
import argparse
import itertools
import subprocess
#import gnupg

def crearDiccionario(chrs, min_length, max_length, outputfile):
    
    inputfile = "archivo.pdf.gpg"                   #archivo cifrado mediante GPG

    salida = "archivo.pdf"                          #archivo donde guardaremos los códigos de error de las palabras probadas


    ############## CONTROL DE ERRORES ####################

    if min_length > max_length:
        print ("[!] ATENCIÓN `min_length` debe ser menor o igual que `max_length`")
        sys.exit()


    #Creamos diccionario en caso de que no exista. output/wordlist.txt por defecto
    if os.path.exists(os.path.dirname(outputfile)) == False:
        os.makedirs(os.path.dirname(outputfile))

    print ('[+] Creando diccionario en `%s`...' % outputfile)
    print ('[i] Tiempo de inicio: %s' % time.strftime('%H:%M:%S'))



    f = open(salida, 'w')
    wordlist = open(outputfile,'w')


    for n in range(min_length, max_length + 1):
        for x in itertools.product(chrs, repeat=n):
            chars = ''.join(x)
            cmdstring = "echo " + chars + "| gpg -d --batch --passphrase-fd 0 " + inputfile                 #probamos combinación mediante gpg
            output = subprocess.Popen(cmdstring,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)   #uso de subprocesos para paralelizar código
            wordlist.write("%s\n" % chars)                                                                  #almacenamos contraseña probada en diccionario
            sys.stdout.write('\r[+] probando `%s`' % chars)
            sys.stdout.flush()
        
    stderroutput=output.communicate()[1]
    stderroutput=stderroutput.decode('utf-8')

    #Comprobamos la salida 
    if stderroutput!="gpg: decryption failed: Bad session key\n":
                f.write("stderroutput:\n"+stderroutput)
                if (stderroutput=="gpg: handle plaintext failed: General error\ngpg: WARNING: message was not integrity protected\n"):
                    f.write("La contraseña es:"+ chars)    
                    print("La contraseña es -->"+chars+ "\n" + stderroutput)
                    f.close()
                    sys.exit(1)
    
    exitcode=output.poll()

    if exitcode==0:                                 #si no existe error
        print("\nThe passphrase is "+chars)
        exit
    else:                                           #si la señal es distinta de 0 (-1)
        print("\n\n\nError al decodificar fichero \n")


    f.close()
    print ('\n[i] Tiempo final: %s' % time.strftime('%H:%M:%S'))


#declaración de un CLI (Command Line Interface) mediante la librería argparse para la lectura de entrada 
#Además

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='Python Wordlist Generator')
    parser.add_argument(
        '-chr', '--chars',
        default= None , help='characters to iterate \nIndique una de las siguientes opciones para la combinación: \n'+
        '1) Numbers \n2) Capital Letters \n3) Lowercase Letters \n4) Numbers + Capital Letters'+
        '\n5) Numbers + Lowercase Letters \n6) Numbers + Capital Letters + Lowercase Letters'
        '\n7) Capital Letters + Lowercase Letters \n8) ASCII Characters')

    parser.add_argument(
        '-max', '--max_length', type=int,
        default=2, help='maximum length of characters')
    
    parser.add_argument(
        '-min', '--min_length', type=int,
        default=1, help='minimum length of characters')
    
    parser.add_argument(
        '-out', '--output',
        default='output/wordlist.txt', help='output of wordlist file.')


    #Personalizamos las opciones de combinación

    args = parser.parse_args()
    if args.chars is None:
        args.chars = string.printable.replace(' \t\n\r\x0b\x0c', '')

    match args.chars:
        case '1':
            args.chars = string.digits
        case '2':
            args.chars = string.ascii_uppercase
        case '3':
            args.chars = string.ascii_lowercase
        case '4':
            args.chars = string.ascii_uppercase + string.digits
        case '5':
            args.chars = string.ascii_lowercase + string.digits
        case '6':
            args.chars = string.ascii_uppercase + string.ascii_uppercase + string.digits
        case '7':
            args.chars = string.ascii_letters
        case '8':
            args.chars = string.ascii_letters + string.digits + string.punctuation

    
    crearDiccionario(args.chars, args.min_length, args.max_length, args.output)
