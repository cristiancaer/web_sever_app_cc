from abc import ABCMeta, abstractmethod
from datetime import datetime
import redis
from werkzeug.security import generate_password_hash,check_password_hash
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
        self.varname_humidity=str(config.get('varname_humidity'))
        self.varname_raspberry_status=str(config.get('varname_raspberry_status'))
        
    def make_connection(self):
        self.db = redis.StrictRedis(host=self.host,
                                port=self.port,
                                db=self.db_name,
                                decode_responses=True)
        self.check_available_connection()
            
    def check_available_connection(self):
        return self.db.ping()

    def put_data_humidity(self,value):
        if self.check_available_connection():
            try:
                ret=self.db.set(self.varname_humidity,value)
            except:
                ret=False

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

    def put_raspberry_status(self,dict_status):
        if self.check_available_connection():
            for key,value in dict_status.items():
                ret=self.db.hset(self.varname_raspberry_status,key,value)
        return ret
    def set_password(self,old_password,new_password):
        ret=False
        if self.check_available_connection():
            if self.check_password(old_password):
                password=generate_password_hash(new_password)
                self.db.set('password',password)
                ret=True
        return ret    
    def check_password(self,password):
        password_db=''
        if self.check_available_connection():
            password_db=self.db.get('password')
        return check_password_hash(password_db,password)

    def get_raspberry_status(self):
        dict_status={}
        if self.check_available_connection():
            dict_status=self.db.hgetall(self.varname_raspberry_status)
        return dict_status
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
    
    def get_humidity(self):
        return self.db.get(self.varname_humidity)

    def dict2str(self,**dictionary):
        info=''
        for key,value in dictionary.items():
                info+='{},{} '.format(key,value)
        info=info[:-1]# para quitar el espacio  del ultimo valor agregado
        return info
    def str2dict(self,string):
        #separar variables
        info=string.split(' ')
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
        return string
    def len_data_flow(self):
        return self.db.hlen(self.varname_flow)
        
if __name__=='__main__':
    config={'host':'localhost',
        'port':6379,
        'db_name':0,
        'timeformat':"%H:%M:%S",
        'varname_flow':'info_mass_flow',
        'varname_humidity': 'humidity',
        'varname_raspberry_status':'raspberry_status'
       }
    db=ConnectionRedis(**config) 
    print("variables in DB:",db.get_name_vars())
    print("last var: ",db.get_last_data_flow_mass())
    print('status_raspberry',db.get_raspberry_status())             
            
    