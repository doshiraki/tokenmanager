from io import StringIO
from tokenman import TokenManager
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request, AuthorizedSession
import json

class TokenCtrlGoogle(TokenManager.TokenData):
    def __init__(self, fileName:str,clientInfo) -> None:
        super().__init__(fileName, clientInfo)
    def load(self):
        self.session = AuthorizedSession(Credentials.from_authorized_user_info(self._load()))

    def create(self, scopes: list):
        flow = InstalledAppFlow.from_client_config({"installed":self.clientInfo}, scopes=scopes)
        flow.run_console()
        self.session = flow.authorized_session()

    def save(self):
        return self._save(json.load(StringIO(self.session.credentials.to_json())))

    def refresh(self, scopes:list):
        self.session.credentials.refresh(Request())

    def getExpiry(self):
        return self.session.credentials.expiry

    def getAccessToken(self):
        return self.session.credentials.token
    
    def getClientInfo(self):
        return TokenCtrlGoogle.ClientInfo

    class ClientInfo(TokenManager.ClientInfo):
        keys = [
            "token_ctrl", #tokenctrlgoogle.TokenCtrlGoogle
            "auth_uri", #https://accounts.google.com/o/oauth2/auth
            "token_uri", #https://oauth2.googleapis.com/token
            "client_id", #cliend id
            "client_secret", #cliend secret
            "redirect_uris", #["http://localhost"]
            "project_id", #google project id
        ]
        def getKeys(self):
            return TokenCtrlGoogle.ClientInfo.keys