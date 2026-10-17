# numero = int("hola!")
# print(numero)

# try
# except
# raise
# finally

# SINTAXIS
# try:
#     #bloque de codigo que quiero tratar de realizar
# except Error:
#     #bloque de codigo que quiero que se ejecute si ocurre la excepcion

try:
    x = 10
    y = 0

    resultado = x / y
except ZeroDivisionError:
    print("No se puede devidir entre 0") 


try:
    numero = int("Hola!")
    print(numero)
except ValueError:
    print("No puedes convertir un alfanumerico en int.") 

try:
    texto = "Hola Profe!"
    num = 22
    frase = texto + num #Solucion: frase = texto + str(num)
except TypeError:
    print("No se pueden mesclar tipos de datos.")

frutas = ["pera","sandia","durazno","melon"]
try:
    print(frutas[4])
except IndexError:
    print("Elemento no existe.")

try:
    estudiante = {
        "nombre": "Pedro",
        "apellido": "Páramo"
    }
    print(estudiante["email"])
except KeyError:
    print("La clave no existe")

def dividir():
    try:
        num1 = int(input("ingresa el primero numero:"))
        num2 = int(input("Ingresa el segundo numero:"))
        resultado = num1/num2
        print(f"El resultado es: {resultado}")
    except ZeroDivisionError:
        print("La calculadora no puede dividirte entre cero.")
    except ValueError:
        print("La calculadora solo permite numeros enteros.")
    except Exception as error:
        print(f"Error inesperado: {error}")
    finally:
        print("Gracias por usar la calculadora!")

dividir()

try:
    bebidas = ["ChocoRon","Piscola","Chimbombo"]
    bebida_deseada = input("Ingresa la bebida que quieres: ")

    if bebida_deseada not in bebidas:
        raise ValueError(f"Esa bebida no esta disponible.") #raise -> levantando una excepción
    else:
        print(f"Tu bebida {bebida_deseada} esta lista")
except ValueError as error:
    print(f"Error: {error}")