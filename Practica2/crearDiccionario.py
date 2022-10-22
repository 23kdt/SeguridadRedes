
#me ha servido como referencia principalmente el siguiente repositorio
#https://github.com/agusmakmun/python-wordlist-generator/blob/master/wgen.py


import os
import sys
import time
import string
import argparse
import itertools
import subprocess
import getopt


#librería para barra de progreso
from tqdm import tqdm



#Función que en función de los parámetros como son los caracteres a usar, longitud mínima y máxima y fichero de salida
#almacenará todas las combinaciones posibles que podemos usar como contraseñas

def crearDiccionario(chrs, min_length, max_length, outputfile):
    
    inputfile = "archivo.pdf.gpg"

    outputdecryptedfile = "archivo.pdf"

    if min_length > max_length:
        print ("[!] ATENCIÓN `min_length` debe ser menor o igual que `max_length`")
        sys.exit()

    if os.path.exists(os.path.dirname(outputfile)) == False:
        os.makedirs(os.path.dirname(outputfile))

    print ('[+] Creando diccionario en `%s`...' % outputfile)
    print ('[i] Tiempo de inicio: %s' % time.strftime('%H:%M:%S'))

    f = open(outputdecryptedfile, 'w')
    wordlist = open(outputfile,'w')


    #tqdm es básicamente una librería para añadir una barra de progreso para visualizar mejor el tiempo restante
    #realmente, esto es en parte bastante ineficente ya que empeora la complejidad y su eficiencia
    #Pero ya que para combinaciones de caracteres grandes es igualmente ineficiente, por lo menos que sea vistoso

    for i in tqdm(range(((max_length+1) - min_length))):
        for n in range(min_length, max_length + 1):
            for x in itertools.product(chrs, repeat=n):
                chars = ''.join(x)
                cmdstring = "echo \"" + chars + "\" | gpg --passphrase-fd 0 -q --batch --allow-multiple-messages --no-tty --output " + outputdecryptedfile + " -d " + inputfile + ";"
                output = subprocess.Popen(cmdstring,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE) # check_output(cmdstring,shell=True,stderr=None)  
                wordlist.write("%s\n" % chars)
                sys.stdout.write('\r[+] saving character `%s`' % chars)
                sys.stdout.flush()
        
    stderroutput=output.communicate()[1]  #must asave it off or it goes bubye
    stderroutput=stderroutput.decode('utf-8')

    if stderroutput!="gpg: decryption failed: Bad session key\n":
                f.write("stderroutput:\n"+stderroutput) #print(stderroutput)
                if (stderroutput=="gpg: handle plaintext failed: General error\ngpg: WARNING: message was not integrity protected\n"):
                    f.write("passphrase is:"+ chars) 
                    print("The passphrase is -->"+chars+ "\n" + stderroutput)
                    f.close()
                    sys.exit(1) 
    exitcode=output.poll() #without calling poll or communicate the exit code will be 
    if exitcode==0:
        print("The passphrase is "+chars)
        exit

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
