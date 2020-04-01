import gramatica as g
import ts as TS
from expresiones import *
from instrucciones import *
from nodos import *

def resolver_cadena(expCad) :
    if isinstance(expCad, ExpresionDobleComilla) :
        return expCad.val
    else :
        print('Error: Expresión cadena no válida')


def resolver_expreision_logica(expLog) :
    global etiqueta

    if isinstance(expLog, ExpresionComparadora) :
        node1 = resolver_expresion_aritmetica(expLog.exp1)
        node2 = resolver_expresion_aritmetica(expLog.exp2)
        if expLog.operador == OPERACION_LOGICA.MAYOR_QUE : 
            verdad = newEtiqueta()
            mentira = newEtiqueta()
            c3d = node1.c3d + node2.c3d + "if " + node1.tem + " > " + node2.tem + " go to " + verdad + '\n'
            c3d = c3d + "go to " + mentira + '\n'  
            return NodoLogico(verdad, mentira, c3d)
        if expLog.operador == OPERACION_LOGICA.MENOR_QUE : 
            verdad = newEtiqueta()
            mentira = newEtiqueta()
            c3d = node1.c3d + node2.c3d + "if " + node1.tem + " < " + node2.tem + " go to " + verdad + '\n'
            c3d = c3d + "go to " + mentira + '\n'  
            return NodoLogico(verdad, mentira, c3d)
        if expLog.operador == OPERACION_LOGICA.IGUAL : 
            verdad = newEtiqueta()
            mentira = newEtiqueta()
            c3d = node1.c3d + node2.c3d + "if " + node1.tem + " == " + node2.tem + " go to " + verdad + '\n'
            c3d = c3d + "go to " + mentira + '\n'  
            return NodoLogico(verdad, mentira, c3d)
        if expLog.operador == OPERACION_LOGICA.DIFERENTE : 
            verdad = newEtiqueta()
            mentira = newEtiqueta()
            c3d = node1.c3d + node2.c3d + "if " + node1.tem + " <> " + node2.tem + " go to " + verdad + '\n'
            c3d = c3d + "go to " + mentira + '\n'  
            return NodoLogico(verdad, mentira, c3d)
    elif isinstance(expLog, ExpresionLogistica) :
        node1 = resolver_expreision_logica(expLog.exp1)
        node2 = resolver_expreision_logica(expLog.exp2)
        if expLog.operador == OPERACION_LOGICA.AND : 
            c3d = node1.c3d + node1.etv + ": \n" + node2.c3d
            verdad = node2.etv 
            mentira = node1.etf + "," + node2.etf
            return NodoLogico(verdad, mentira, c3d)
        if expLog.operador == OPERACION_LOGICA.OR : 
            c3d = node1.c3d + node1.etf + ": \n" + node2.c3d
            verdad = node1.etv + "," + node2.etv
            mentira = node2.etf
            return NodoLogico(verdad, mentira, c3d)
    elif isinstance(expLog, ExpresionNegadora) :
        node = resolver_expreision_logica(expLog.exp)
        if expLog.operador == OPERACION_LOGICA.NOT : 
            c3d = node.c3d
            verdad = node.etf
            mentira = node.etv
            return NodoLogico(verdad, mentira, c3d)
    

def resolver_expresion_aritmetica(expNum) :
    global temporal

    if isinstance(expNum, ExpresionBinaria) :
        node1 = resolver_expresion_aritmetica(expNum.exp1)
        node2 = resolver_expresion_aritmetica(expNum.exp2)
        if expNum.operador == OPERACION_ARITMETICA.MAS : 
            tem = newTemporal()
            c3d = tem + "=" + node1.tem + "+" + node2.tem + '\n'
            c3d = node1.c3d + node2.c3d + c3d
            return NodoAritmetico(tem, c3d)
        if expNum.operador == OPERACION_ARITMETICA.MENOS : 
            tem = newTemporal()
            c3d = tem + "=" + node1.tem + "-" + node2.tem + '\n'
            c3d = node1.c3d + node2.c3d + c3d
            return NodoAritmetico(tem, c3d)
        if expNum.operador == OPERACION_ARITMETICA.POR : 
            tem = newTemporal()
            c3d = tem + "=" + node1.tem + "*" + node2.tem + '\n'
            c3d = node1.c3d + node2.c3d + c3d
            return NodoAritmetico(tem, c3d)
        if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO : 
            tem = newTemporal()
            c3d = tem + "=" + node1.tem + "/" + node2.tem + '\n'
            c3d = node1.c3d + node2.c3d + c3d
            return NodoAritmetico(tem, c3d)
    elif isinstance(expNum, ExpresionNegativo) :
        node = resolver_expresion_aritmetica(expNum.exp)
        tem = newTemporal()
        c3d = tem + "=" + "-" + node.tem + '\n'
        c3d = node.c3d + c3d
        return NodoAritmetico(tem, c3d)
    elif isinstance(expNum, ExpresionNumero) :
        return NodoAritmetico(expNum.val, "")
    elif isinstance(expNum, ExpresionIdentificador) :
        return NodoAritmetico(expNum.id, "")


def procesar_instrucciones(instrucciones) :
    ## lista de instrucciones recolectadas
    c3d = ""

    for instr in instrucciones :
        if isinstance(instr, Imprimir) : 
            c3d = c3d + procesar_imprimir(instr).c3d
        elif isinstance(instr, If) : 
            c3d = c3d + procesar_if(instr).c3d
        elif isinstance(instr, IfElse) : 
            node = procesar_if_else(instr)
            c3d = c3d + node.c3d
        else : print('Error: instrucción no válida')
    
    return c3d


def procesar_imprimir(instr) :
    return NodoSentencia('<' + resolver_cadena(instr.cad) + '>' + '\n')

def procesar_if(instr) :
    nodeLogico = resolver_expreision_logica(instr.expLogica)
    c3d = nodeLogico.c3d + nodeLogico.etv + ": \n " + procesar_instrucciones(instr.instrucciones) + nodeLogico.etf + ": \n"
    return NodoIf(c3d)

def procesar_if_else(instr) :
    global etiqueta

    nodeLogico = resolver_expreision_logica(instr.expLogica)
    salida = newEtiqueta()
    c3d = nodeLogico.c3d + nodeLogico.etv + ": \n" + procesar_instrucciones(instr.instrIfVerdadero) + "go to " + salida + '\n'
    c3d = c3d + nodeLogico.etf + ": \n" + procesar_instrucciones(instr.instrIfFalso) + salida + ": \n"
    return NodoSubIf(salida, c3d)

temporal = 0
etiqueta = 0

def newTemporal():
    global temporal

    temporal = temporal + 1
    return "t" + str(temporal)

def newEtiqueta():
    global etiqueta

    etiqueta = etiqueta + 1
    return "L" + str(etiqueta)

f = open("./entrada.txt", "r")
input = f.read()

instrucciones = g.parse(input)

print("======================")
print("|Codigo 3 Direcciones|")
print("====================== \n")

codigo = procesar_instrucciones(instrucciones)

f = open("./salida.txt", "w")
f.write(codigo)
f.close()

print(codigo)

print("=====================================================")
print("|Se escribio todo el codigo en el archivo salida.txt|")
print("=====================================================")