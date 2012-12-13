import LogError
import datetime
import SQLite
from Dominio import Dominio
import urllib

import Imagem
import Link
import Texto
import Video

#from BeautifulSoup import BeautifulSoup

class Site:
    
    def __init__(self):    
        self.nomeDominio = ""
        self.descricaoURL = ""
        self.quantidadeLinks = 0
        self.quantidadeTextos = 0
        self.quantidadeImagens = 0
        self.quantidadeVideos = 0
        self.timeStamp = datetime.datetime.now()
        self.SQLiteConnection = SQLite.SQLite()
        
    def Insert(self):
        try:            
            if(self.nomeDominio == "" or self.descricaoURL == ""):
                raise (" O nome do dominio e a descricao da URL nao podem ser vazio.") 
            
           
            dominio = Dominio()
            dominio.nome = self.nomeDominio
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            dominio.SQLiteConnection = self.SQLiteConnection
            
            dominios = dominio.Select()
            if(dominios.__len__() <= 0):
                dominio.Insert()
                
            sqlQuery = " insert into TB_SITES values('"
            sqlQuery = sqlQuery + self.nomeDominio + "', '"
            sqlQuery = sqlQuery + self.descricaoURL + "', "
            sqlQuery = sqlQuery + str(self.quantidadeLinks) + ", "
            sqlQuery = sqlQuery + str(self.quantidadeTextos) + ", "
            sqlQuery = sqlQuery + str(self.quantidadeImagens) + ", "
            sqlQuery = sqlQuery + str(self.quantidadeVideos) + ", "
            sqlQuery = sqlQuery + "datetime('now')) "
            
            if(not self.SQLiteConnection.Execute(sqlQuery)):
                raise("Erro ao inserir site.")
            
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)       
        
        finally:
            self.SQLiteConnection.Disconnect()
            
    def Update(self):
        try:
            if(self.nomeDominio == "" or self.descricaoURL == ""):
                raise("O nome do dominio e a descricao da URL nao podem ser vazio.")
           
            sqlQuery = " update TB_SITES set "
            sqlQuery = sqlQuery + "QT_LINKS = " + self.quantidadeLinks + ", "
            sqlQuery = sqlQuery + "QT_TEXTOS = " + self.quantidadeTextos + ", "
            sqlQuery = sqlQuery + "QT_IMAGENS = " + self.quantidadeImagens + ", "
            sqlQuery = sqlQuery + "QT_VIDEOS = " + self.quantidadeVideos + ", "
            sqlQuery = sqlQuery + "DT_TIME_STAMP = datetime('now')) "             
            sqlQuery = sqlQuery + " where NM_DOMINIO = "" + self.nomeDominio + """
            sqlQuery = sqlQuery + " and DS_URL = "" + self.descricaoURL + """
            
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            if(not self.SQLiteConnection.Execute(sqlQuery)):
                raise("Erro ao atualizar site.")
            
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)       
        
        finally:
            self.SQLiteConnection.Disconnect() 

    def Delete(self):
        try:
            if(self.nomeDominio == "" or self.descricaoURL == ""):
                raise("O nome do dominio e a descricao da URL nao podem ser vazio.")
           
            sqlQuery = " delete from TB_SITES "             
            sqlQuery = sqlQuery + " where NM_DOMINIO = "" + self.nomeDominio + """
            sqlQuery = sqlQuery + " and DS_URL = "" + self.descricaoURL + """
            
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            if(not self.SQLiteConnection.Execute(sqlQuery)):
                raise("Erro ao deletar site.")
            
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)       
        
        finally:
            self.SQLiteConnection.Disconnect() 


    def ToObject(self, row):
        try:
            site = Site()
            site.nomeDominio =  row[0]
            site.descricaoURL = row[1]
            site.quantidadeLinks = row[2]
            site.quantidadeTextos = row[3]
            site.quantidadeImagens = row[4]
            site.quantidadeVideos = row[5]            
            site.timeStamp = row[6]
            return site  
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)         
        
    def Select(self):
        try:           
            sqlQuery = " select * from TB_SITES "
            sqlQueryTemp = " where "
            
            if(self.nomeDominio != ""):             
                sqlQuery = sqlQuery + sqlQueryTemp + " NM_DOMINIO = '" + self.nomeDominio + "'"
                sqlQueryTemp = " and "
                
            if(self.descricaoURL != ""):             
                sqlQuery = sqlQuery + sqlQueryTemp + " DS_URL = '" + self.descricaoURL + "'"            
            
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
            
            rows = self.SQLiteConnection.Select(sqlQuery)
            sites = []
            for row in rows:
                site = self.ToObject(row)
                sites.append(site)
                
            return sites 
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)               
        finally:
            self.SQLiteConnection.Disconnect()
    
    def ReadUrl(self, url):
        try:
            self.nomeDominio = self.GetDominioDescription(url)
            self.descricaoURL = url
            if(not self.SQLiteConnection.IsConnected()):
                if(not self.SQLiteConnection.Connect()):
                    raise("Erro ao conectar na base.")
                    
            sites = self.Select()
            
            if(sites.__len__() <= 0):
                self.timeStamp = datetime.datetime.now()    
                self.Insert()     
            
            html = urllib.request.urlopen(url)
            page = str(html.read())
            self.BuscaVideos(page)
            self.BuscaTexto(page)
            self.BuscaLink(page)
            self.BuscaImg(page)
            
                          
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)         
        
        
    def GetDominioDescription(self, url):
            dom = urllib.request.urlparse(url)
            if(dom[0] == "http" or dom[0] == "https"):                
                return dom[1]
            else:
                return dom[2]


    def BuscaImg(self,page):           
            try:
                tempPage = page
                startIndexImage = tempPage.find("<img")
                while(startIndexImage >= 0):
                    tempPage = tempPage[startIndexImage:]
                    endIndexImage = tempPage.find("/>") + 2
                    imageHtml = tempPage[0:endIndexImage]
                    tempPage = tempPage[endIndexImage:]
                    startIndexImage = tempPage.find("<img")
                    image = Imagem.Imagem()
                    image.nomeDominio = self.nomeDominio
                    image.descricaoURL = self.descricaoURL
                    image.sequencia = image.GetSequencia()
                    indexSrc = imageHtml.find("src=") + 5
                    src = imageHtml[indexSrc:]
                    indexSrc = src.find("\"")
                    if(indexSrc < 1):
                        indexSrc = src.find("'")
                        if(indexSrc < 1):
                            indexSrc = src.find(" ")
                    src = src[0:indexSrc]
                    image.descricaoImagem = src.replace("'","")
                    descricaoImageTemp = image.descricaoImagem 
                    indexExtencao = descricaoImageTemp .find(".")                   
                    while indexExtencao >= 0:                         
                        descricaoImageTemp = descricaoImageTemp[indexExtencao + 1:]
                        indexExtencao = descricaoImageTemp .find(".") 
                    if(descricaoImageTemp != "" and descricaoImageTemp != image.descricaoImagem):
                        image.extencao = descricaoImageTemp
                        
                    image.Insert()
                    
                    
            except KeyError:
                pass
            
    def BuscaLink(self,page):           
            try:
                tempPage = page
                startIndexImage = tempPage.find("<a")
                while(startIndexImage >= 0):
                    tempPage = tempPage[startIndexImage:]
                    endIndexImage = tempPage.find("</a>") + 4
                    if(endIndexImage < 0):
                        endIndexImage = tempPage.find("/>") + 2    
                    linkHtml = tempPage[0:endIndexImage]
                    tempPage = tempPage[endIndexImage:]
                    startIndexImage = tempPage.find("<a")
                    link = Link.Link()
                    link.nomeDominio = self.nomeDominio
                    link.descricaoURL = self.descricaoURL
                    link.sequencia = link.GetSequencia()
                    indexHref = linkHtml.find("href=\\")
                    if(indexHref > 0):
                        indexHref = indexHref + 7
                    else:
                        indexHref = linkHtml.find("href=") 
                        if(indexHref > 0):
                            indexHref = indexHref + 6
                    if(indexHref > 0):
                        href = linkHtml[indexHref:]
                        indexHref = href.find("\"")
                        if(indexHref < 1):
                            indexHref = href.find("\\'")
                            if(indexHref < 1):
                                indexHref = href.find("'")
                                if(indexHref < 1):
                                    indexHref = href.find(" ")
                        href = href[0:indexHref]
                        link.linkURL = href.replace("'","")
                        linkDominio = self.GetDominioDescription(link.linkURL)
                        if(linkDominio == self.nomeDominio):
                            link.isInterno = True
                            self.ReadUrl(link.linkURL)
                        else:
                            link.isInterno = False
                        link.Insert()
                        
                    
            except KeyError:
                pass
            
            
    def BuscaTexto(self,page):           
            try:
                tempPage = page
                startIndexImage = tempPage.find("<span")
                while(startIndexImage >= 0):
                    tempPage = tempPage[startIndexImage:]
                    endIndexImage = tempPage.find("</span>") + 7                   
                    textoHtml = tempPage[0:endIndexImage]
                    tempPage = tempPage[endIndexImage:]
                    startIndexImage = tempPage.find("<span")
                    texto = Texto.Texto()
                    texto.nomeDominio = self.nomeDominio
                    texto.descricaoURL = self.descricaoURL
                    texto.sequencia = texto.GetSequencia()
                    indexSpan = textoHtml.find(">") + 1
                    if(indexSpan > 0):                        
                        span = textoHtml[indexSpan:endIndexImage - 7]
                        texto.tamanho = span.__len__()  
                        if(texto.tamanho > 0):                      
                            texto.Insert()
                        
                    
            except KeyError:
                pass
            
            
    def BuscaVideos(self,page):           
            try:
                tempPage = page
                startIndexImage = tempPage.find("<embed")
                while(startIndexImage >= 0):
                    tempPage = tempPage[startIndexImage:]
                    endIndexImage = tempPage.find("/>") + 2
                    imageHtml = tempPage[0:endIndexImage]
                    tempPage = tempPage[endIndexImage:]
                    startIndexImage = tempPage.find("<embed")
                    video = Video.Video()
                    video.nomeDominio = self.nomeDominio
                    video.descricaoURL = self.descricaoURL
                    video.sequencia = video.GetSequencia()
                    indexSrc = imageHtml.find("src=") + 5
                    src = imageHtml[indexSrc:]
                    indexSrc = src.find("\"")
                    if(indexSrc < 1):
                        indexSrc = src.find("'")
                        if(indexSrc < 1):
                            indexSrc = src.find(" ")
                    src = src[0:indexSrc]
                    video.descricaoVideo = src.replace("'","")
                    descricaoVideoTemp = video.descricaoVideo 
                    indexExtencao = descricaoVideoTemp.find(".")                   
                    while indexExtencao >= 0:                         
                        descricaoVideoTemp = descricaoVideoTemp[indexExtencao + 1:]
                        indexExtencao = descricaoVideoTemp.find(".") 
                    if(descricaoVideoTemp != "" and descricaoVideoTemp != video.descricaoVideo):
                        video.extencao = descricaoVideoTemp
                        
                    video.Insert()
                    
                    
            except KeyError:
                pass
