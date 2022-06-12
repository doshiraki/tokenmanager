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
        print(self.clientInfo.me())
        flow = InstalledAppFlow.from_client_config({"installed":self.clientInfo.me()}, scopes=scopes)
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
        _default = {
                TokenManager.ClientInfo.token_ctrl.__name__: None, #tokenctrlgoogle.TokenCtrlGoogle
                TokenManager.ClientInfo.auth_uri.__name__: "https://accounts.google.com/o/oauth2/auth",
                TokenManager.ClientInfo.token_uri.__name__: "https://oauth2.googleapis.com/token",
                TokenManager.ClientInfo.client_id.__name__: None, #cliend id
                TokenManager.ClientInfo.client_secret.__name__: None, #cliend secret
                TokenManager.ClientInfo.redirect_uris.__name__: None, #["urn:ietf:wg:oauth:2.0:oob"]
            }
        def getDefault(self)->dict:
            return TokenCtrlGoogle.ClientInfo._default

