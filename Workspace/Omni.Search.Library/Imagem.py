import LogError
import datetime
import SQLite
import Site
class Imagem:
    
    def __init__(self):
        self.nomeDominio = ""
        self.descricaoURL = ""
        self.descricaoImagem = ""
        self.sequencia = 0
        self.tamanho = 0
        self.extencao = ""        
        self.timeStamp = datetime.datetime.now()
        self.SQLiteConnection = SQLite.SQLite()
    def GetSequencia(self):        
        try:           
            retorno = 1
            sqlQuery = " select MAX(CD_SEQUENCIA) from TB_IMAGENS where NM_DOMINIO = '" + self.nomeDominio + "' AND DS_URL = '" + self.descricaoURL + "'"
            
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
            
            sqlQuery = " insert into TB_IMAGENS values('"
            sqlQuery = sqlQuery + self.nomeDominio + "', '"
            sqlQuery = sqlQuery + self.descricaoURL + "', "            
            sqlQuery = sqlQuery + str(self.sequencia) + ", '"
            sqlQuery = sqlQuery + self.descricaoImagem + "', "
            sqlQuery = sqlQuery + str(self.tamanho) + ", '"
            sqlQuery = sqlQuery + self.extencao + "', "            
            sqlQuery = sqlQuery + "datetime('now')) "
            
            if(not self.SQLiteConnection.Execute(sqlQuery)):
                raise("Erro ao inserir imagem.")
            
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)       
        
        finally:
            self.SQLiteConnection.Disconnect()
            
    def Update(self):
        try:
            if(self.nomeDominio == "" or self.descricaoURL == "" or self.sequencia <= 0):
                raise("O nome do dominio, a descricao da URL e a sequencia nao podem ser vazio.")
           
            sqlQuery = " update TB_IMAGENS set "
            sqlQuery = sqlQuery + "QT_TAMANHO = " + self.tamanho + ", "
            sqlQuery = sqlQuery + "DS_EXTENCAO = '" + self.extencao + "', "
            sqlQuery = sqlQuery + "DT_TIME_STAMP = datetime('now')) "             
            sqlQuery = sqlQuery + " where NM_DOMINIO = '" + self.nomeDominio + "'"
            sqlQuery = sqlQuery + " and DS_URL = '" + self.descricaoURL + "'"
            sqlQuery = sqlQuery + " and CD_SEQUENCIA = " + self.sequencia
            
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            if(not self.SQLiteConnection.Execute(sqlQuery)):
                raise("Erro ao atualizar imagem.")
            
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)       
        
        finally:
            self.SQLiteConnection.Disconnect() 


    def Delete(self):
        try:
            if(self.nomeDominio == "" or self.descricaoURL == "" or self.sequencia <= 0):
                raise("O nome do dominio, a descricao da URL e a sequencia nao podem ser vazio.")
           
            sqlQuery = " delete from TB_IMAGENS "             
            sqlQuery = sqlQuery + " where NM_DOMINIO = '" + self.nomeDominio + "'"
            sqlQuery = sqlQuery + " and DS_URL = '" + self.descricaoURL + "'"
            sqlQuery = sqlQuery + " and CD_SEQUENCIA = " + self.sequencia 
            
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            if(not self.SQLiteConnection.Execute(sqlQuery)):
                raise("Erro ao deletar imagem.")
            
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)       
        
        finally:
            self.SQLiteConnection.Disconnect() 


    def ToObject(self, row):
        try:
            imagem = Imagem()
            imagem.nomeDominio =  row[0]
            imagem.descricaoURL = row[1]
            imagem.sequencia = row[2]
            imagem.tamanho = row[3]
            imagem.extencao = row[4]            
            imagem.timeStamp = row[5]
            return imagem  
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)         

    def Select(self):
        try:           
            sqlQuery = " select * from TB_IMAGENS "
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
            imagens = []
            for row in rows:
                imagem = self.ToObject(row)
                imagens.append(imagem)
                
            return imagens 
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)               
        finally:
            self.SQLiteConnection.Disconnect()