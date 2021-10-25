import queue
import requests
from threading import Thread
from queue import Queue
from time import sleep
from bs4 import BeautifulSoup
class Communication(Thread):
    def __init__(self,url,que_mass_flow) -> None:
        super().__init__()
        self.url=url
        self.que=que_mass_flow
        self.running=True
        self.separator='---'
    def get_last_data(self):
        res= requests.get(self.url)
        info={}
        if res.text!='None':
            soup=BeautifulSoup(res.text,'html.parser')
            data=soup.find_all(class_='data')
            for tag in data:
                tag=tag.text.strip()
                key,value=tag.split(self.separator)
                info.setdefault(key,value)
        return info
    def run(self) -> None:
        while self.running:
            info=self.get_last_data()
            print(info)
            if info:
                self.que.put(info)
            else:
                print('no data')
            sleep(2)
class AnalogOput(Thread):
    def __init__(self, minInput,maxIput,minOutput,maxOutput,que_mass_flow) -> None:
        super().__init__()
        self.runing=True
        self.minInput=minInput
        self.maxInput=maxIput
        self.minOutput=minOutput
        self.maxOutput=maxOutput
        self.que_mass_flow=que_mass_flow
    def convert_value(self,value):
        output=self.minOutput +(self.maxOutput-self.minOutput)/(self.maxInput-self.minInput)*(value-self.minInput)
        return output
    def run(self):
        while self.runing:
            info_mass_flow=self.que_mass_flow.get()
            mass_flow=info_mass_flow.get('mass_flow')
            print(mass_flow)

if __name__=='__main__':
    que_mass_flow=Queue()
    url='http://127.0.0.1:5000/connection/data_available/'
    comm=Communication(url,que_mass_flow)
    comm.start()
    analogOutput=AnalogOput(0,1,0,5,que_mass_flow)
    analogOutput.start()
    while True:
        c=input("press c to exit")
        if c=='c':
            comm.running=False
            analogOutput.runing=False
            break

