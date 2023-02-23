#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 00:10:58 2023

@author: zak
"""

from ayesa_pronunciar import ayesa_operador
from reconocer_cliente import cliente_transcript
import warnings
warnings.filterwarnings('ignore')

def main():
    ao = ayesa_operador()
    ct = cliente_transcript()
    texto_bienvenido_1 = 'Bienvenido a centro clientes Ayesa, por el español pronuncia 1, por el inglés pronuncia 2'
    ao.pronunciar(texto_bienvenido_1, 'es')    
    texto_bienvenido_2 = 'Welcome to the call center of Ayesa, for Spanish pronounce uno, for English pronounce dos'
    ao.pronunciar(texto_bienvenido_2, 'en')
    client_reply = ct.trsncript_solicitud('es-ES',1)
    tentativas = 2
    test_idioma = tentativas
    test_palabras = tentativas
    idioma_por_defecto = 'es-ES'
    while test_idioma != 4:
        if (client_reply != None):
            if (client_reply[0] == "uno") or (client_reply[0] == "dos"):
                if client_reply[0] == "uno":
                    idioma = 'es-ES'
                    text = 'Describe brevemente lo que quieres hacer'       
                    ao.pronunciar(text, idioma)
                    test_solicitud = 3
                    ct.procesamiento_recursivo_solicitud(test_solicitud,idioma,7,ao,ct)
                elif client_reply[0] == "dos":
                    # caso de inglés no tratado
                    idioma = 'en-US'
                    text = 'Please describe briefly what you want to do'       
                    ao.pronunciar(text, idioma)  
                test_idioma = 4
            else:
                test_palabras = test_palabras - 1
                if test_palabras > 0:
                    ao.pronunciar("Por favor pronuncia solamente 1 o 2", 'es-ES')
                    client_reply = ct.trsncript_solicitud(idioma_por_defecto,1)
                elif test_palabras == 0:
                    ao.pronunciar("Esto es su ultima tentativa, Por favor pronuncia solamente 1 o 2", 'es-ES')  
                    client_reply = ct.trsncript_solicitud(idioma_por_defecto,1)
                elif test_palabras < 0:
                    ao.finalizar_llamada(ao,idioma_por_defecto)
                    break;
        elif client_reply == None:
            test_idioma = test_idioma - 1
            if test_idioma > 0:
                ao.pronunciar("Por favor repite lo que has dicho claramente", 'es-ES')
                client_reply = ct.trsncript_solicitud(idioma_por_defecto,1)
            elif test_idioma == 0:
                ao.pronunciar("Esto es su ultima tentativa Por favor repite lo que has dicho claramente", 'es-ES')  
                client_reply = ct.trsncript_solicitud(idioma_por_defecto,1)
            elif test_idioma < 0:
                ao.finalizar_llamada(ao,idioma_por_defecto)
                break;


if __name__ == "__main__":
    main()