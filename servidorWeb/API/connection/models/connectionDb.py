from abc import ABCMeta, abstractmethod
from datetime import datetime
import redis
class ConnectionDb(metaclass=ABCMeta):
    @abstractmethod
    def check_available_connection(self):
        pass
    @abstractmethod
    def make_connection(self):
        pass

    @abstractmethod
    def put_data_flow_mass(self,**flow_mass_info):
        pass
    @abstractmethod
    def get_last_data_flow_mass(self):
        pass
    @abstractmethod
    def get_all_data_flow_mass(self):
        pass
    @abstractmethod
    def config_db(self,**config):
        pass
class ConnectionRedis(ConnectionDb):
    def __init__(self,**config):
        self.config_db(**config)
        self.make_connection()
    def config_db(self,**config):
        self.host=config.get('host')
        self.db_name=config.get('db_name')
        self.port=config.get('port')
        self.timeformat=config.get('timeformat')
        self.varname_flow=str(config.get('varname_flow'))
        
    def make_connection(self):
        self.db = redis.StrictRedis(host=self.host,
                                port=self.port,
                                db=self.db_name)
        self.check_available_connection()
            
    def check_available_connection(self):
        return self.db.ping()
    def put_data_flow_mass(self, **flow_mass_info):
        if self.check_available_connection():
            info=self.dict2str(**flow_mass_info)
            try: 
                date=datetime.now().strftime(self.timeformat)   
                ret= self.db.hset(self.varname_flow,date,info)
            except:
                print("not found timeformat")
                ret=False
            return ret
    def get_all_data_flow_mass(self):
        data=sorted(self.db.hgetall(self.varname_flow).items())
        data={"{}".format(self.binary2utf8(index)):self.str2dict(data) for index,data in data }
        return data
    def get_last_data_flow_mass(self):
        data=sorted(self.db.hgetall(self.varname_flow).items())
        if len(data):
            time,data=data[-1]#last data
            data=self.str2dict(data)
            data.setdefault('time',self.binary2utf8(time))
        else:
            data={}
        return data
    def dict2str(self,**dictionary):
        info=''
        for key,value in dictionary.items():
                info+='{},{} '.format(key,value)
        info=info[:-1]# para quitar el espacio  del ultimo valor agregado
        return info
    def str2dict(self,string):
        #separar variables
        info=string.decode('utf-8').split(' ')
        #formar diccionario
        data=dict(data.split(',') for data in info)
        return data
    def get_name_vars(self):
        return self.db.keys()
    def clear_var(self):
        self.db.delete(self.varname_flow)
    def delete_var(self,var):
        self.db.delete(var)
    def binary2utf8(self,string):
        return string.decode('utf-8')
    def len_data_flow(self):
        return self.db.hlen(self.varname_flow)
        
if __name__=='__main__':
    config={'host':'localhost',
        'port':6379,
        'db_name':0,
        'timeformat':"%H:%M:%S",
        'varname_flow':'info_mass_flow'
       }
    db=ConnectionRedis(**config) 
    print("variables in DB:",db.get_name_vars())
    print("last var: ",db.get_last_data_flow_mass())              
            
    