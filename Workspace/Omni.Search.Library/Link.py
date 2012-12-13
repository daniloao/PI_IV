import LogError
import datetime
import SQLite
import Site
class Link:
    
    def __init__(self):
        self.nomeDominio = ""
        self.descricaoURL = ""
        self.sequencia = 0        
        self.linkURL = "" 
        self.isInterno = False       
        self.timeStamp = datetime.datetime.now()
        self.SQLiteConnection = SQLite.SQLite()
        
    def GetSequencia(self):        
        try:           
            retorno = 1
            sqlQuery = " select MAX(CD_SEQUENCIA) from TB_LINKS where NM_DOMINIO = '" + self.nomeDominio + "' AND DS_URL = '" + self.descricaoURL + "'"
            
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            rows = self.SQLiteConnection.Select(sqlQuery)
            
            for row in rows:
                if(row[0] != None):
                    retorno = row[0] + 1
            
            return retorno 
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)               
        finally:
            self.SQLiteConnection.Disconnect()

    def Insert(self):
        try:
            if(self.nomeDominio == "" or self.descricaoURL == "" or self.sequencia <= 0):
                raise("O nome do dominio, a descricao da URL e a sequencia nao podem ser vazio.")
           
            site = Site.Site()
            site.nomeDominio = self.nomeDominio
            site.descricaoURL = self.descricaoURL
            
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            site.SQLiteConnection = self.SQLiteConnection
            
            sites = site.Select()
            if(sites.__len__() <= 0):
                site.Insert()
            
            self.sequencia = self.GetSequencia()
            sqlQuery = " insert into TB_LINKS values('"
            sqlQuery = sqlQuery + self.nomeDominio + "', '"
            sqlQuery = sqlQuery + self.descricaoURL + "', "
            sqlQuery = sqlQuery + str(self.sequencia) + ", '"
            sqlQuery = sqlQuery + str(self.linkURL) + "', "
            if(self.isInterno):
                sqlQuery = sqlQuery + "1 , "
            else:
                sqlQuery = sqlQuery + "0 , "            
            sqlQuery = sqlQuery + "datetime('now')) "
            
            if(not self.SQLiteConnection.Execute(sqlQuery)):
                raise("Erro ao inserir link.")
            
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)       
        
        finally:
            self.SQLiteConnection.Disconnect()
            
    def Update(self):
        try:
            if(self.nomeDominio == "" or self.descricaoURL == "" or self.sequencia <= 0):
                raise("O nome do dominio, a descricao da URL e a sequencia nao podem ser vazio.")
           
            sqlQuery = " update TB_LINKS set "
            sqlQuery = sqlQuery + "DS_LINK_URL = '" + self.linkURL + "', "
            sqlQuery = sqlQuery + "FL_INTERNO = " + self.isInterno + ", "
            sqlQuery = sqlQuery + "DT_TIME_STAMP = datetime('now')) "             
            sqlQuery = sqlQuery + " where NM_DOMINIO = '" + self.nomeDominio + "'"
            sqlQuery = sqlQuery + " and DS_URL = '" + self.descricaoURL + "'"
            sqlQuery = sqlQuery + " and CD_SEQUENCIA = " + self.sequencia
            
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            if(not self.SQLiteConnection.Execute(sqlQuery)):
                raise("Erro ao atualizar link.")
            
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)       
        
        finally:
            self.SQLiteConnection.Disconnect() 


    def Delete(self):
        try:
            if(self.nomeDominio == "" or self.descricaoURL == "" or self.sequencia <= 0):
                raise("O nome do dominio, a descricao da URL e a sequencia nao podem ser vazio.")
           
            sqlQuery = " delete from TB_LINKS "             
            sqlQuery = sqlQuery + " where NM_DOMINIO = '" + self.nomeDominio + "'"
            sqlQuery = sqlQuery + " and DS_URL = '" + self.descricaoURL + "'"
            sqlQuery = sqlQuery + " and CD_SEQUENCIA = " + self.sequencia 
            
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            if(not self.SQLiteConnection.Execute(sqlQuery)):
                raise("Erro ao deletar link.")
            
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)       
        
        finally:
            self.SQLiteConnection.Disconnect() 


    def ToObject(self, row):
        try:
            link = Link()
            link.nomeDominio =  row[0]
            link.descricaoURL = row[1]
            link.sequencia = row[2]
            link.linkURL = row[3]
            link.isInterno = row[4]            
            link.timeStamp = row[5]
            return link  
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)         

    def Select(self):
        try:           
            sqlQuery = " select * from TB_LINKS "
            sqlQueryTemp = " where "
            
            if(self.nomeDominio != ""):             
                sqlQuery = sqlQueryTemp + " NM_DOMINIO = '" + self.nomeDominio + "'"
                sqlQueryTemp = " and "
                
            if(self.descricaoURL != ""):             
                sqlQuery = sqlQueryTemp + " DS_URL = '" + self.descricaoURL + "'"
                sqlQueryTemp = " and "
                
            if(self.sequencia > 0):             
                sqlQuery = sqlQueryTemp + " CD_SEQUENCIA = " + self.sequencia             
            
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            rows = self.SQLiteConnection.Select(sqlQuery)
            links = []
            for row in rows:
                link = self.ToObject(self,row)
                links.append(link)
                
            return links
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)               
        finally:
            self.SQLiteConnection.Disconnect()