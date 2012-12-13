import LogError
import datetime
import SQLite
import Site
class Texto:
    
    def __init__(self):
        self.nomeDominio = ""
        self.descricaoURL = ""
        self.sequencia = 0
        self.tamanho = 0
        self.font = ""
        self.cor = ""
        self.tamanhoFont = 0        
        self.timeStamp = datetime.datetime.now()
        self.SQLiteConnection = SQLite.SQLite()
        
    def GetSequencia(self):        
        try:           
            retorno = 1
            sqlQuery = " select MAX(CD_SEQUENCIA) from TB_TEXTOS where NM_DOMINIO = '" + self.nomeDominio + "' AND DS_URL = '" + self.descricaoURL + "'"
            
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
            sqlQuery = " insert into TB_TEXTOS values('"
            sqlQuery = sqlQuery + self.nomeDominio + "', '"
            sqlQuery = sqlQuery + self.descricaoURL + "', "
            sqlQuery = sqlQuery + str(self.sequencia) + ", "
            sqlQuery = sqlQuery + str(self.tamanho) + ", '"
            sqlQuery = sqlQuery + self.font + "', '"
            sqlQuery = sqlQuery + self.cor + "', "
            sqlQuery = sqlQuery + str(self.tamanhoFont) + ", "            
            sqlQuery = sqlQuery + "datetime('now')) "
            
            if(not self.SQLiteConnection.Execute(sqlQuery)):
                raise("Erro ao inserir texto.")
            
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)       
        
        finally:
            self.SQLiteConnection.Disconnect()
            
    def Update(self):
        try:
            if(self.nomeDominio == "" or self.descricaoURL == "" or self.sequencia <= 0):
                raise("O nome do dominio, a descricao da URL e a sequencia nao podem ser vazio.")
           
            sqlQuery = " update TB_TEXTOS set "
            sqlQuery = sqlQuery + "QT_TAMANHO = " + self.tamanho + ", "
            sqlQuery = sqlQuery + "DS_FONT = '" + self.font + "', "
            sqlQuery = sqlQuery + "DS_COR = '" + self.cor + "', "
            sqlQuery = sqlQuery + "QT_TAMANHO_FONT = " + self.tamanhoFont + ", "
            sqlQuery = sqlQuery + "DT_TIME_STAMP = datetime('now')) "             
            sqlQuery = sqlQuery + " where NM_DOMINIO = '" + self.nomeDominio + "'"
            sqlQuery = sqlQuery + " and DS_URL = '" + self.descricaoURL + "'"
            sqlQuery = sqlQuery + " and CD_SEQUENCIA = " + self.sequencia
            
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            if(not self.SQLiteConnection.Execute(sqlQuery)):
                raise("Erro ao atualizar texto.")
            
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)       
        
        finally:
            self.SQLiteConnection.Disconnect() 


    def Delete(self):
        try:
            if(self.nomeDominio == "" or self.descricaoURL == "" or self.sequencia <= 0):
                raise("O nome do dominio, a descricao da URL e a sequencia nao podem ser vazio.")
           
            sqlQuery = " delete from TB_TEXTOS "             
            sqlQuery = sqlQuery + " where NM_DOMINIO = '" + self.nomeDominio + "'"
            sqlQuery = sqlQuery + " and DS_URL = '" + self.descricaoURL + "'"
            sqlQuery = sqlQuery + " and CD_SEQUENCIA = " + self.sequencia 
            
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            if(not self.SQLiteConnection.Execute(sqlQuery)):
                raise("Erro ao deletar texto.")
            
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)       
        
        finally:
            self.SQLiteConnection.Disconnect() 


    def ToObject(self, row):
        try:
            texto = Texto()
            texto.nomeDominio =  row[0]
            texto.descricaoURL = row[1]
            texto.sequencia = row[2]
            texto.tamanho = row[3]
            texto.font = row[4]
            texto.cor = row[5]
            texto.tamanhoFont = row[6]            
            texto.timeStamp = row[7]
            return texto
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)         

    def Select(self):
        try:           
            sqlQuery = " select * from TB_TEXTOS "
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
            textos = []
            for row in rows:
                texto = self.ToObject(self,row)
                textos.append(texto)
                
            return textos
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)               
        finally:
            self.SQLiteConnection.Disconnect()