import numpy as np
from numpy.random import  randint
from threading import Thread
import requests
from time import sleep
import json
class PutData:
    def __init__(self,url) -> None:
        self.url=url
        self.format={'mass_flow':'12.2','humidity': '12.1'}
    def sent(self,dato):
        res= requests.post(self.url,data=dato)
        return res.status_code==200
class GenerarDatos(Thread):
    url='http://127.0.0.1:5000/connection/put/'
    running=True
    putData=PutData(url)
    def run(self):
        while self.running:
            data=randint(100)
            data={'mass_flow':data,'humidity': '12.1'}
            print('sent',self.putData.sent(data))
            
        
            sleep(4)
if __name__=='__main__':
    generador=GenerarDatos()
    generador.start()
    while True:
       
        input=input('pres c to exit: ')
        
        if input=='c':
            generador.running=False
            sleep(1)
            break