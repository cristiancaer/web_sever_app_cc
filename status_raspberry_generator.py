import requests
from threading import Thread
from time import sleep
def status_raspberry_generator(is_running):
    url='http://127.0.0.1:5000/connection/put_raspberry_status/'
    dict_status={ 'status {}'.format(i):i for i in range(10)}
    sess=requests.session()
    while is_running():
        res=sess.post(url,json=dict_status)
        print(res)
        sleep(4)
def run():
    running=True
    work=Thread(target=status_raspberry_generator,args=(lambda:running,))
    work.setDaemon(True)
    work.start()
    while running:
        key=input("press q to exit: \n")
        if key=='q':
            running=False

if __name__=='__main__':
    run()