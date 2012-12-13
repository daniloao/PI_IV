import os
import datetime

class LogError:
    
    @staticmethod
    def Save(pErr):
        try:
            logFile = open(os.getcwd() + "\\ErrorLog.txt", "w")
            logFile.write("Error " + datetime.datetime.now())
            logFile.write(str(pErr))
            logFile.write("-------------------------------------")
            logFile.write("")
            
        except:
            pass
        finally:
            logFile.close()