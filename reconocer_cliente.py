import speech_recognition as sr
import numpy as np
import time



class cliente_transcript():
    def __init__(self):
        self.r = sr.Recognizer()
        self.m = sr.Microphone() 
        print("A moment of silence, please...")
        with self.m as source: self.r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(self.r.energy_threshold))

    def trsncript_solicitud(self, idioma, palabras):
        with self.m as source: self.r.adjust_for_ambient_noise(source)      
        try:
            print("Say something!")
            with self.m as source: audio = self.r.listen(source, phrase_time_limit=palabras)
            print("Got it! Now to recognize it...")
            try:
                # reconocer utilizando google recogniser
                value = self.r.recognize_google(audio,language=idioma)
                # we need some special handling here to correctly print unicode characters to standard output
                if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                    print(u"You said {}".format(value).encode("utf-8"))
                    client_reply = value.split()
                else:  # this version of Python uses unicode for strings (Python 3+)
                    print("You said {}".format(value))
                    client_reply = value.split()
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
                client_reply = None
                time.sleep(4)
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
                client_reply = None
                time.sleep(4)
        except KeyboardInterrupt:
            pass
        return client_reply
    
    def procesamiento_recursivo_solicitud(self,test_solicitud,idioma,palabras,ao,ct):
        client_reply = self.trsncript_solicitud(idioma, palabras)
        if (client_reply != None): # si el cliente ha dicho algo
            candidates = []
            for element in client_reply:
                if element in "facturación":
                    candidates.append("servicio_facturacion")
                # here we can add a dictionary to find similar words or add words refering to other services
                if element in "cliente":
                    candidates.append("servicio_cliente")    
            candidates = list(np.unique(np.array(candidates)))
            if candidates == []:
               text = 'Por favor reduce la descripción de su trámite a lo esencial'       
               ao.pronunciar(text, idioma)
               test_solicitud = 2
               self.procesamiento_recursivo_solicitud(test_solicitud,idioma,palabras,ao,ct)
            else:
                if len(candidates) == 1: # en el caso de un servicio
                    if candidates[0] == "servicio_facturacion":
                        test_finalizacion = ao.servicio_facturacion(idioma,palabras,ao,ct)
                    elif candidates[0] == "servicio_cliente":
                        test_finalizacion = ao.servicio_cliente(idioma,palabras,ao,ct)
                    if test_finalizacion >= 0:
                        ao.cancelacion_repeticio(idioma,palabras,ao,ct)
                    else:
                        ao.finalizar_llamada(ao,idioma)
                else: # en el caso de varios servicios
                    text = "Por favor elige entre estos servicios repitiendo su nombre"
                    for servicio in candidates:
                        text = text + servicio;
                    ao.pronunciar(text, idioma)
                    test_solicitud = 3
                    self.procesamiento_recursivo_solicitud(test_solicitud,idioma,palabras,ao,ct)                 
        elif client_reply == None:
            test_solicitud = test_solicitud - 1
            if test_solicitud != 0:
                ao.pronunciar("Por favor repite lo que has dicho claramente", idioma)
                self.procesamiento_recursivo_solicitud(test_solicitud,idioma,palabras,ao,ct)
            elif test_solicitud == 0:
                ao.pronunciar("Esto es su ultima tentativa Por favor repite lo que has dicho claramente", idioma)  
                self.procesamiento_recursivo_solicitud(test_solicitud,idioma,palabras,ao,ct)
            elif test_solicitud < 0:
                ao.finalizar_llamada(ao,idioma)
