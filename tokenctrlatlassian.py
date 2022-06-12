import imp
from io import StringIO
from random import randint

import httplib2
from tokenman import TokenManager
from oauth2client.client import OAuth2Credentials, OAuth2WebServerFlow
import datetime

import json

class TokenCtrlAtlassian(TokenManager.TokenData):
    def __init__(self, fileName:str,clientInfo) -> None:
        super().__init__(fileName, clientInfo)
    def load(self):
        self.credentials = OAuth2Credentials.from_json(json.dumps(self._load()))

    def create(self, scopes: list):
        offilne = "offline_access"
        if not offilne in scopes:
            #refresh_token get
            scopes.append(offilne)
        flow = OAuth2WebServerFlow(
            self.clientInfo.client_id(),
            self.clientInfo.client_secret(),
            " ".join(scopes),
            auth_uri=self.clientInfo.auth_uri(),
            token_uri=self.clientInfo.token_uri(),
            audience="api.atlassian.com",
            prompt="consent",
        )
        url = flow.step1_get_authorize_url(
            self.clientInfo.redirect_uris(),
            randint(100000,999999)
        )
        print("Confire Url Page: {}".format(url))
        print("Then press Enter.")
        self.credentials:OAuth2Credentials = flow.step2_exchange(input())
        

    def save(self):
        return self._save(json.load(StringIO(self.credentials.to_json())))

    def refresh(self, scopes:list):
        self.credentials.refresh(httplib2.Http())

    def getExpiry(self):
        return self.credentials.token_expiry

    def getAccessToken(self):
        return self.credentials.access_token
    
    def getClientInfo(self):
        return TokenCtrlAtlassian.ClientInfo

    class ClientInfo(TokenManager.ClientInfo):
        keys = [
            TokenManager.ClientInfo.token_ctrl.__name__, #tokenctrlatlassian.TokenCtrlAtlassian
            TokenManager.ClientInfo.auth_uri.__name__, #https://auth.atlassian.com/authorize
            TokenManager.ClientInfo.token_uri.__name__, #https://auth.atlassian.com/oauth/token
            TokenManager.ClientInfo.client_id.__name__, #cliend id
            TokenManager.ClientInfo.client_secret.__name__, #cliend secret
            TokenManager.ClientInfo.redirect_uris.__name__, #["http://localhost"]
        ]
        def getKeys(self):
            return TokenCtrlAtlassian.ClientInfo.keys
