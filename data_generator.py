import numpy as np
from numpy.random import  randint
from threading import Thread
import requests
from time import sleep
import json
class PutData:
    def __init__(self,url) -> None:
        self.url=url
        self.format={'mass_flow':'12.2'}# example of how the data is store
    def sent(self,dato):
        res= requests.post(self.url,data=dato)
        return res.status_code==200
class GenerarDatos(Thread):
    url='http://127.0.0.1:5000/connection/put_flow/'
    running=True
    putData=PutData(url)
    def run(self):
        while self.running:
            data=randint(9,60)
            data={'mass_flow':data}
            print('sent',self.putData.sent(data))
            sleep(4)

if __name__=='__main__':
    generador=GenerarDatos()
    generador.start()
    while True:
       
        key=input('pres c to exit: ')
        
        if key=='c':
            generador.running=False
            sleep(1)
            break