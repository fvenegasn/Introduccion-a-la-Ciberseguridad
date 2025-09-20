from pwn import *
# Para debug del socket utilizamos:
context.log_level = 'debug'
# Analice las diferencias entre usar o no el debug
    # Utilizando debug: Muestra información sobre los bytes que se envían y se reciben
    # No utilizando debug: Sólo muestra lo que la librería loggea en su nivel de log por defecto

# Nos conectamos utilizando remote
con = remote("ic.catedras.linti.unlp.edu.ar", 10001)

# para quitar el texto que no nos interesa (banner),
# leemos hasta justo antes de la cuenta, es decir, hasta ":\n"
con.readuntil("resolver esta cuenta:\n")

# Leemos hasta el salto de línea, la cuenta deseada
cuenta = con.readline()

print(type(cuenta))
print(cuenta)

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

#time.sleep(2) # Si se descomenta esta línea por ejemplo, se puede ver 
# cómo el mensaje cambia ya que no responde en 1 segundo

# Enviamos la respuesta de la cuenta, como bytes:
con.send((str(resultado) + "\n").encode())

# Imprimimos toda la respuesta del servidor
print(con.readall())
