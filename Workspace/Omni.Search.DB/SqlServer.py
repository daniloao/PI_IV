import pyodbc
import Settings
import LogError 

class SqlServer:
    
    def __init__(self):
        self._connection_string = Settings.Settings.ConnectionString()
        self._connection = None
        self._cursor = None
        self._is_internal_connection = False
        
    def ConnectionString(self):        
        return self._connection_string 
    
    def Connect(self):
        try:
            self._connection = pyodbc.connect(self.ConnectionString())
            self._cursor = self._connection.cursor()
            return True
        except Exception, err:
            LogError.LogError.Save(err) 
            raise Exception(err)
    
    def Disconnect(self):
        try:
            self._connection = None
            self._cursor = None
            return True
        except Exception, err:
            LogError.LogError.Save(err)
            raise Exception(err) 
        
        def IsConnected(self):
            if(self._connection is None or self._cursor is None):
                return False
            
            return True
        
        def Select(self, pQuery):
            try:
                if(not self.IsConnected(self)):
                    if(not self.Connect()):
                        raise("Error in connect")
                    
                    self._is_internal_connection = True
                    
                self._cursor.execute(pQuery)
                return self._cursor.fetchall()            
                    
            except Exception, err:
                LogError.LogError.Save(err)
                raise Exception(err)
            
            finally:
                if(self._is_internal_connection):
                    self.Disconnect()
                    self._is_internal_connection = False
                    
        def Execute(self, pQuery):
            try:
                if(not self.IsConnected(self)):
                    if(not self.Connect()):
                        raise("Error in connect")
                    
                    self._is_internal_connection = True
                    
                self._cursor.execute(pQuery)
                self._cursor.commit()            
                return True 
            
            except Exception, err:
                LogError.LogError.Save(err)
                if(not self._cursor is None):
                    self._cursor.rollback()
                
                raise Exception(err)
            
            finally:
                if(self._is_internal_connection):
                    self.Disconnect()
                    self._is_internal_connection = False
            