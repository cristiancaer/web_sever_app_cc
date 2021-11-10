import shlex
import subprocess
from  threading import Thread
from os import system
from time import sleep
class connectionClient:
    COMMAND_CHECK_INTERFACE=shlex.split("nmcli d")
    STATES_INTERFACE=(' connected',' disconnected',' unknown')
    MESSAGE_STATUS_INTERFACE='The  interface is '
    MESSAGE_STATUS_CONNECTION='The conneciton is '
    MESSAGE_ADVICE_RISE_UP_CONN='Try (nmcli con up name_conn) in console to rise up connection'
    MESSAGE_CONN_EXIST='The name connection exist is '
    message_status=None
    all_is_ok=False
    advice_message=None
    
    def __init__(self,name_conn='local',client_addr='112.168.1.2',type_interface='ethernet'):
        self.info_connection={'name_conn': name_conn,
                     'client_conn_addr':client_addr,
                     'conn_exist':False,
                     'ping_success':False,
                     'type_interface':type_interface,
                     'interface_status':'unknown'
                     ,'conn_is_up':False}
        self.COMMAND_CONN_EXIST=shlex.split('nmcli con show {}'.format(self.info_connection.get('name_conn')))
        self.COMMAND_PING_CLIENT=shlex.split("ping -c 3 {}".format(self.info_connection.get('client_conn_addr')))
        self.check_conn()
    def run_command(self,command):
        output=subprocess.run(command,check=False,encoding='utf-8',capture_output=True)
        type_stdout=output.returncode
        stdout=output.stdout
        run_ok=False
        if type_stdout==0:# Type stout oput,if type==2 it is an error stdout
            run_ok=True
        return run_ok,stdout
    def update_info_connection(self):
        self.info_connection['conn_exist']=self.check_conn_exist()
        if self.info_connection['conn_exist']:   
            run_ok,stdout=self.run_command(self.COMMAND_CHECK_INTERFACE)
            for line in stdout.split('\n'):
                if line.find(self.info_connection.get('type_interface'))!=-1:
                # check connection status is up
                    if self.info_connection.get('name_conn') in line:
                        self.info_connection['conn_is_up']=True
                        self.info_connection['ping_success']=self.check_ping_successful()
                    else:
                        self.info_connection['conn_is_up']=False
                        self.info_connection['ping_success']=False
                    for state in self.STATES_INTERFACE:
                        if state in line:
                            self.info_connection['interface_status']=state.strip()# delete space in blanck
                            break
    def check_conn(self):
        self.update_info_connection()
        self.advice_message=''
        self.message_status=''
        if self.info_connection.get('conn_exist'):
            if self.info_connection.get('interface_status')=='connected':
                if self.info_connection.get('conn_is_up'):
                    if not self.info_connection.get('ping_success'):
                        self.message_status=self.MESSAGE_STATUS_CONNECTION+'UP. But ping was unsuccessfull'
                        self.advice_message='Check address client' + ' or Try unplug and plug the cable'
                else:
                    self.message_status=self.MESSAGE_STATUS_CONNECTION+'Down'
                    self.advice_message='Try unplug and plug the cable or '+self.MESSAGE_ADVICE_RISE_UP_CONN

            else:
                self.message_status=self.MESSAGE_CONN_EXIST+'True. But '+self.MESSAGE_STATUS_INTERFACE+'Disconnected'
                self.advice_message='Try unplug and plug the cable'+'\n or \n ''Try (nmcli con up name_conn) in console to rise up connection'
        else:
            self.message_status=self.MESSAGE_CONN_EXIST+'False'
            self.advice_message='Check name connection'
    def get_info_conn(self):
        self.update_info_connection()
        return self.info_connection
    def check_ping_successful(self):
        run_ok,stdout=self.run_command(self.COMMAND_PING_CLIENT)
        # find index of received word to know how many package from ping was Not lost
        index=stdout.find('received')
        package_received=int(stdout[index-2:index].strip())
        if  package_received==0:
            ping_ok=False
        else:
            ping_ok=True
        return ping_ok
    def check_conn_exist(self):
        run_ok,_=self.run_command(self.COMMAND_CONN_EXIST)
        
        if run_ok:
            exist=True
        else:
            exist=False
        return exist
def run(is_running):
    client=connectionClient(name_conn='local',client_addr='112.168.1.2',type_interface='ethernet')
    info=client.get_info_conn()
    buffer=''
    while True:    
        client.check_conn()
        sleep(2)
        message_now=str(client.message_status)+str(client.advice_message)
        if True:
            system('clear')
            print(client.info_connection)
            print('message connection status: ')
            print(client.message_status)
            print('advice message')
            print(client.advice_message)
            buffer=message_now
        if not is_running():
            break
if __name__=='__main__':
    is_running=True
    work=Thread(target=run,args=(lambda:is_running,))
    work.start()
    while True:
        key=input('press q to close: ')
        if key=='q':
            is_running=False
            break
