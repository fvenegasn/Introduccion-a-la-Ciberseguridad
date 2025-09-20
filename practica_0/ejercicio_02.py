from pwn import *

def calcular_resultado(cuenta):
    """
    Se generaliza el comportamiento para los N cálculos que se realizan
    """

    #print(type(cuenta))
    #print(cuenta)

    # Pasamos los bytes a string, para poder realizar la cuenta
    cuenta = cuenta.decode()

    # Split convierte una cadena de texto en una lista, utilizando como separador los
    # espacios en blanco
    cuenta = cuenta.split() # ['297', '+', '155']

    # Convierto a entero los operandos
    op1 = int(cuenta[0])
    op2 = int(cuenta[2])
    operador = cuenta[1]

    # Sumo multiplico o resto según el operador
    if operador == '+':
        resultado = op1 + op2
    elif operador == '*':
        resultado = op1 * op2
    else:
        resultado = op1 - op2
    return resultado

# Para debug del socket utilizamos:
context.log_level = 'debug'
# Analice las diferencias entre usar o no el debug
    # Utilizando debug: Muestra información sobre los bytes que se envían y se reciben
    # No utilizando debug: Sólo muestra lo que la librería loggea en su nivel de log por defecto

# Nos conectamos utilizando remote
con = remote("ic.catedras.linti.unlp.edu.ar", 10002)

# para quitar el texto que no nos interesa (banner),
# leemos hasta justo antes de la cuenta, es decir, hasta ":\n"
con.readuntil("Resuelvan estas sumas para obtener la flag!:\n")
# No puedo generalizar la lectura del banner, el resto si

# Hasta que no encuentre la flag
while True:
    # leemos hasta justo antes de la cuenta, es decir, hasta ":\n"
    linea = con.recvline(timeout=1.5)

    # Si la línea contiene un operando
    if any(op in linea.decode() for op in ["+", "-", "*"]):
        # Calculo el resultado
        resultado = calcular_resultado(linea)
        # Enviamos la respuesta de la cuenta, como bytes:
        con.send((str(resultado) + "\n").encode())

    # Si encontre la flag, corto la ejecución
    elif b"la flag" in linea:
        break
    
# Imprimimos toda la respuesta del servidor
print(con.readall())
