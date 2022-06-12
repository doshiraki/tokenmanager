from abc import abstractmethod
import importlib
import yaml
import datetime
import os
import inspect
class TokenManager:
    class ClientInfo:
        def __init__(self, clientInfo) -> None:
            self.clientInfo = clientInfo
        def me(self):
            return self.clientInfo
        def _getProps(self, name:str):
            if not name in self.getKeys():
                raise Exception("no props")
            return self.clientInfo[name]
        def token_ctrl(self)->str:
            return self._getProps(inspect.currentframe().f_code.co_name)
        def client_id(self)->str:
            return self._getProps(inspect.currentframe().f_code.co_name)
        def client_secret(self)->str:
            return self._getProps(inspect.currentframe().f_code.co_name)
        def redirect_uris(self, idx:int=0)->str:
            return self._getProps(inspect.currentframe().f_code.co_name)[idx]
        def auth_uri(self)->str:
            return self._getProps(inspect.currentframe().f_code.co_name)
        def token_uri(self)->str:
            return self._getProps(inspect.currentframe().f_code.co_name)
        def project_id(self)->str:
            return self._getProps(inspect.currentframe().f_code.co_name)
        @abstractmethod
        def getKeys(self):
            pass

    class YamlIO:
        def __init__(self, yamlFile:str) -> None:
            self.yamlFile = yamlFile
        def load(self):
            with open(self.yamlFile, "r") as f:
                tokenInfo = yaml.load(f, yaml.UnsafeLoader)
            return tokenInfo
        def save(self, data):
            with open(self.yamlFile, "w") as f:
                yaml.dump(data, f)

    class TokenData:
        def __init__(self, fileName, clientInfo) -> None:
            self.yamlIO = TokenManager.YamlIO(fileName)
            self.clientInfo:TokenManager.ClientInfo = self.getClientInfo()(clientInfo)
        def _load(self):
            return self.yamlIO.load()
        def _save(self, data):
            self.yamlIO.save(data)

        @abstractmethod
        def load(self):
            pass

        @abstractmethod
        def create(self, scopes: list):
            pass

        @abstractmethod
        def save(self):
            pass

        @abstractmethod
        def refresh(self, scopes:list):
            pass

        @abstractmethod
        def getExpiry(self):
            pass

        @abstractmethod
        def getAccessToken(self):
            pass

        @abstractmethod
        def getClientInfo(self):
            pass

    def __init__(self, tokenCtrlConf:str, scopes:list, fileName:str) -> None:
        self.scopes = scopes
        clientInfo:TokenManager.ClientInfo = TokenManager.YamlIO(tokenCtrlConf).load()
        *package, name = clientInfo["token_ctrl"].split(".")
        getClass = eval("lambda x:x."+name)
        tokenCtrl = getClass(importlib.import_module(".".join(package)))
        self.td:TokenManager.TokenData = tokenCtrl(fileName, clientInfo)
        if os.path.exists(fileName):
            self.td.load()
        else:
            self.td.create(self.scopes)
            self.td.save()
    
    def getAccessToken(self):
        if self.td.getExpiry() < datetime.datetime.utcnow():
            self.td.refresh(self.scopes)
            self.td.save()
        return self.td.getAccessToken()
