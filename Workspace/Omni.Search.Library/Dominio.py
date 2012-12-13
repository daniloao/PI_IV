import LogError
import datetime
import SQLite


class Dominio:
    
    def __init__(self):
        self.nome = ""
        self.tipo = ""
        self.timeStamp = datetime.datetime.now()
        self.SQLiteConnection = SQLite.SQLite()
        
    def Insert(self):
        try:
            if(self.nome == ""):
                raise("O nome nao pode ser vazio.")
           
            sqlQuery = " insert into tb_dominios values('"
            sqlQuery = sqlQuery + self.nome + "', '"
            sqlQuery = sqlQuery + self.tipo + "', "
            sqlQuery = sqlQuery + "datetime('now')) "
            
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            if(not self.SQLiteConnection.Execute(sqlQuery)):
                raise("Erro ao inserir dominio.")
            
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)       
        
        finally:
            self.SQLiteConnection.Disconnect() 
            
    def Update(self):
        try:
            if(self.nome == ""):
                raise("O nome nao pode ser vazio.")
           
            sqlQuery = " update tb_dominios set "
            sqlQuery = sqlQuery + "DS_TIPO = '" + self.tipo + "', "
            sqlQuery = sqlQuery + "DT_TIME_STAMP = datetime('now')) "             
            sqlQuery = sqlQuery + " where NM_DOMINIO = '" + self.nome + "'"
            
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            if(not self.SQLiteConnection.Execute(sqlQuery)):
                raise("Erro ao atualizar dominio.")
            
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)       
        
        finally:
            self.SQLiteConnection.Disconnect() 
            
            
    def Delete(self):
        try:
            if(self.nome == ""):
                raise("O nome nao pode ser vazio.")
           
            sqlQuery = " delete from tb_dominios "             
            sqlQuery = sqlQuery + " where NM_DOMINIO = '" + self.nome + "'"
            
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            if(not self.SQLiteConnection.Execute(sqlQuery)):
                raise("Erro ao deletar dominio.")
            
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)       
        
        finally:
            self.SQLiteConnection.Disconnect()
            
    def Select(self):
        try:           
            sqlQuery = " select * from tb_dominios "
            sqlQueryTemp = " where "
            
            if(self.nome != ""):             
                sqlQuery = sqlQuery + sqlQueryTemp + " NM_DOMINIO = '" + self.nome + "'"
                sqlQueryTemp = " and "
                
            if(self.tipo != ""):             
                sqlQuery = sqlQuery + sqlQueryTemp + " DS_TIPO = '" + self.tipo + "'"            
            
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            rows = self.SQLiteConnection.Select(sqlQuery)
            dominios = []
            for row in rows:
                dominio = self.ToObject(row)
                dominios.append(dominio)
                
            return dominios                        
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)               
        finally:
            self.SQLiteConnection.Disconnect()
            
    def ToObject(self, row):
        try:
            dominio = Dominio()
            dominio.nome = row[0]
            dominio.tipo = row[1]
            dominio.timeStamp = row[2]
            return dominio  
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)
        