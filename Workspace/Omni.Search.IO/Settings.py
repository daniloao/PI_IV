import os
from xml.dom.minidom import parse
import LogError
class Settings:
    _connection_string = ""
        
    @staticmethod
    def ConnectionString():        
        if(Settings._connection_string == ""):
            Settings.Load()
                        
        return Settings._connection_string
    
        
    @staticmethod
    def Load():
        try:
            Settings._settings_path = os.getcwd() + "\\Omni.Search.Settings.xml"
            settingsFile = parse(open(Settings._settings_path))
            Settings._connection_string = settingsFile.getElementsByTagName("ConnectionString")[0].firstChild.data
        except ValueError:
            LogError.LogError.Save(ValueError)
            raise Exception(ValueError)
