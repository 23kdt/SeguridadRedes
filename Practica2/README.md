
archivo.pdf.gpg es archivo cifrado con "gpg". Sin embargo, no me acuerdo de la clave. Me acuerdo que la clave tenía sólo caracteres en minúsculas, pero nada más. ¿Me podéis ayudar a encontrar la clave?

Entregrable

Se debe realizar un programa que averigüe la clave con la que se cifró el archivo dado. Este programa se puede realizar en cualquier lenguaje de programación. Se debe incluir en el entregable:

- Un README explicando cómo instalar y ejecutar el programa en un entorno GNU/Linux.
- El código fuente del programa.

Se valorará:

- La rapidez con la que se encuentra la clave: cuanto más rápido mejor.
- La limpieza del código y del contenido del proyecto.

# EJECUCIÓN

                      python3 practica2_brute.py (-min “x”) (-max “y”) (-chr “z”) (-out “file”)

Si ejecutamos el comando con - -h / -help nos mostrará información extra sobre los parámetros de entrada (todos opcionales ya que hay valores por defecto).

Mi idea ha sido realizar un ataque de fuerza bruta para contraseñas de longitud y formatos variables, y almacenar todas las combinaciones probadas en un diccionario.

Los parametros -min y -max determinan la longitud mínima y máxima de las contraseñas a probar.

El parámetro -chr tiene distintas opciones. Si introducimos caracteres, realizará pruebas con la combinación de dichos caracteres (por ejemplo, si introducimos “-min 3 – max 3 -chr abc” como parámetro realizará pruebas con las combinaciones “aaa”, ”bbb”, ”ccc”, ”aab”, ”aac”, ”aba”, ”abb” , etc. ). Sin embargo, y como indico en el panel de ayuda, si introducimos un dígito utilizará un formato predeterminado (como letras minúsculas, mayúsculas, dígitos, símbolos o combinados).
