#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 00:26:10 2023

@author: zak
"""
import os
from gtts import gTTS
import time
from datetime import datetime


class ayesa_operador:
    def __init__(self):
        pass
    
    def pronunciar(self, frase, idioma):
        myobj = gTTS(text=frase, lang=idioma, slow=False)      
        myobj.save("audio.mp3")
        os.system("play audio.mp3")
        
    def servicio_facturacion(self,idioma,palabras,ao,ct):
        self.pronunciar('Está en el servicio de facturación, para efectuar un pago pronuncia 1, para quejas pronuncia 2', idioma)
        tentativas = 2
        test_elecion = tentativas
        test_palabras = tentativas
        client_elecion = ct.trsncript_solicitud(idioma, 1)
        while test_elecion != 4:
            if (client_elecion != None):
                if (client_elecion[0] == "uno") or (client_elecion[0] == "dos"):
                    if client_elecion[0] == "uno":
                        text = 'Por favor espere que te ponemos en contacto con uno de nuestros operadores'       
                        self.pronunciar(text, idioma)
                        time.sleep(4)
                    elif client_elecion[0] == "dos":
                        text = 'Por favor, puedes decir sus quejas y será transmitida automáticamente a nuestro departamento'       
                        self.pronunciar(text, idioma)  
                        queja = ct.trsncript_solicitud(idioma,100)
                        archivo = "servicio_facturas/quejas/quejas_servicios_facturas_"+str(datetime.now())+ ".txt"
                        with open(archivo,"w") as quejas_fichero:
                            for palabra in (queja):
                                quejas_fichero.write(palabra)
                                quejas_fichero.write(' ')
                        quejas_fichero.close()    
                    test_elecion = 4
                else:
                    test_palabras = test_palabras - 1
                    if test_palabras > 0:
                        ao.pronunciar("Por favor pronuncia solamente 1 o 2", idioma)
                        client_elecion = ct.trsncript_solicitud(idioma,1)
                    elif test_palabras == 0:
                        self.pronunciar("Esto es su ultima tentativa, Por favor pronuncia solamente 1 o 2", 'es-ES')  
                        client_elecion = ct.trsncript_solicitud(idioma,1)
                    elif test_palabras < 0:
                        break;
            elif client_elecion == None:
                test_elecion = test_elecion - 1
                if test_elecion > 0:
                    self.pronunciar("Por favor repite lo que has dicho claramente", idioma)
                    client_elecion = ct.trsncript_solicitud(idioma,1)
                elif test_elecion == 0:
                    self.pronunciar("Esto es su ultima tentativa Por favor repite lo que has dicho claramente", idioma)  
                    client_elecion = ct.trsncript_solicitud(idioma,1)
                elif test_elecion < 0:
                    break;
        return test_elecion


    def servicio_cliente(self,idioma,palabras,ao,ct):
        self.pronunciar('Está en el servicio de cliente, para sugerencias pronuncia 1, para quejas pronuncia 2', idioma)
        tentativas = 2
        test_elecion = tentativas
        test_palabras = tentativas
        client_elecion = ct.trsncript_solicitud(idioma, 1)
        while test_elecion != 4:
            if (client_elecion != None):
                if (client_elecion[0] == "uno") or (client_elecion[0] == "dos"):
                    if client_elecion[0] == "uno":
                        text = 'Por favor, puedes decir sus sugerencias y será transmitida automáticamente a nuestro departamento'       
                        self.pronunciar(text, idioma)  
                        sugerencia = ct.trsncript_solicitud(idioma,100)
                        archivo = "servicio_cliente/sugerencias/sugerencias_servicio_cliente_"+str(datetime.now())+ ".txt"
                        with open(archivo,"w") as sugerencias_fichero:
                            for palabra in (sugerencia):
                                sugerencias_fichero.write(palabra)
                                sugerencias_fichero.write(' ')
                        sugerencias_fichero.close()
                    elif client_elecion[0] == "dos":
                        text = 'Por favor, puedes decir sus quejas y será transmitida automáticamente a nuestro departamento'       
                        self.pronunciar(text, idioma)  
                        queja = ct.trsncript_solicitud(idioma,100)
                        archivo = "servicio_cliente/quejas/quejas_servicio_cliente_"+str(datetime.now())+ ".txt"
                        with open(archivo,"w") as quejas_fichero:
                            for palabra in (queja):
                                quejas_fichero.write(palabra)
                                quejas_fichero.write(' ')
                        quejas_fichero.close()                          
                    test_elecion = 4
                else:
                    test_palabras = test_palabras - 1
                    if test_palabras > 0:
                        ao.pronunciar("Por favor pronuncia solamente 1 o 2", idioma)
                        client_elecion = ct.trsncript_solicitud(idioma,1)
                    elif test_palabras == 0:
                        self.pronunciar("Esto es su ultima tentativa, Por favor pronuncia solamente 1 o 2", 'es-ES')  
                        client_elecion = ct.trsncript_solicitud(idioma,1)
                    elif test_palabras < 0:
                        break;
            elif client_elecion == None:
                test_elecion = test_elecion - 1
                if test_elecion > 0:
                    self.pronunciar("Por favor repite lo que has dicho claramente", idioma)
                    client_elecion = ct.trsncript_solicitud(idioma,1)
                elif test_elecion == 0:
                    self.pronunciar("Esto es su ultima tentativa Por favor repite lo que has dicho claramente", idioma)  
                    client_elecion = ct.trsncript_solicitud(idioma,1)
                elif test_elecion < 0:
                    break;
        return test_elecion
   
    def cancelacion_repeticio(self,idioma,palabras,ao,ct):
        self.pronunciar('Si quieres buscar un nuevo tramite pronuncia 1, si quires finalizar la llamada pronuncia 2', idioma)
        client_feedback = ct.trsncript_solicitud(idioma, palabras)
        tentativas = 2
        test_neuva_solicitud = tentativas
        test_palabras = tentativas
        while test_neuva_solicitud != 4:
            test_neuva_solicitud = tentativas
            if (client_feedback != None):
                if (client_feedback[0] == "uno") or (client_feedback[0] == "dos"):
                    if client_feedback[0] == "uno":
                        text = 'Describe brevemente su tramite'       
                        ao.pronunciar(text, idioma)
                        test_solicitud = 3
                        ct.procesamiento_recursivo_solicitud(test_solicitud,idioma,7,ao,ct)
                    elif client_feedback[0] == "dos":
                        self.finalizar_llamada(ao, idioma)  
                        break;
                    test_neuva_solicitud = 4
                else:
                    test_palabras = test_palabras - 1
                    if test_palabras > 0:
                        ao.pronunciar("Por favor pronuncia solamente 1 o 2", idioma)
                        client_feedback = ct.trsncript_solicitud(idioma,1)
                    elif test_palabras == 0:
                        ao.pronunciar("Esto es su ultima tentativa, Por favor pronuncia solamente 1 o 2", 'es-ES')  
                        client_feedback = ct.trsncript_solicitud(idioma,1)
                    elif test_palabras < 0:
                        self.finalizar_llamada(ao,idioma)
                        break;
            elif client_feedback == None:
                test_neuva_solicitud = test_neuva_solicitud - 1
                if test_neuva_solicitud > 0:
                    ao.pronunciar("Por favor repite lo que has dicho claramente", 'es-ES')
                    client_feedback = ct.trsncript_solicitud(idioma,1)
                elif test_neuva_solicitud == 0:
                    ao.pronunciar("Esto es su ultima tentativa Por favor repite lo que has dicho claramente", 'es-ES')  
                    client_feedback = ct.trsncript_solicitud(idioma,1)
                elif test_neuva_solicitud < 0:
                    self.finalizar_llamada(ao,idioma)
                    break;
    
    def finalizar_llamada(self,ao,idioma):
        self.pronunciar('Llamada finalizada, esperamos que hemos resuelto su trámite satisfactoriamente', idioma)

        