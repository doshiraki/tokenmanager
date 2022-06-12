from tokenman import TokenManager
from msal import ConfidentialClientApplication
import datetime

class TokenCtrlMicrosoft(TokenManager.TokenData):
    def __init__(self, fileName:str,clientInfo) -> None:
        super().__init__(fileName, clientInfo)
        tenant_id = self.clientInfo.tenant_id()
        auth_uri = self.clientInfo.auth_uri()
        if auth_uri == TokenCtrlMicrosoft.ClientInfo._default["auth_uri"]:
            auth_uri += tenant_id
        self.app = ConfidentialClientApplication(
            self.clientInfo.client_id(),
            authority=auth_uri,
        )

    def load(self):
        self.credentials = self._load()

    def create(self, scopes: list):
        code = self.app.initiate_auth_code_flow(
            scopes,
            redirect_uri=self.clientInfo.redirect_uris()
        )
        print("Please visit this URL to authorize this application: " + code["auth_uri"])
        print("Enter the authorization code: ", end="")
        self.credentials = self.app.acquire_token_by_authorization_code(
            input(),
            scopes, 
            self.clientInfo.redirect_uris(),
            data=code,
            params={"client_secret":self.clientInfo.client_secret()}
        )

    def save(self):
        return self._save(self.credentials)

    def refresh(self, scopes:list):
        self.credentials = self.app.acquire_token_by_refresh_token(self.credentials["refresh_token"], scopes)

    def getExpiry(self):
        expiry = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(self.credentials["id_token_claims"]["exp"]))
        #print(expiry)
        return expiry

    def getAccessToken(self):
        return self.credentials["access_token"]

    def getClientInfo(self):
        return TokenCtrlMicrosoft.ClientInfo

    class ClientInfo(TokenManager.ClientInfo):
        _default = {
                TokenManager.ClientInfo.token_ctrl.__name__: None, #tokenctrlmicrosoft.TokenCtrlMicrosoft
                TokenManager.ClientInfo.auth_uri.__name__: "https://login.microsoftonline.com/",
                TokenManager.ClientInfo.tenant_id.__name__: None,
                TokenManager.ClientInfo.client_id.__name__: None, #(Application (client) ID)
                TokenManager.ClientInfo.client_secret.__name__: None, #(Secret Value)
                TokenManager.ClientInfo.redirect_uris.__name__: ["msalc93a2a4e-9aba-4513-9424-e794706a2260://auth"], #["http://localhost"]
            }
        def getDefault(self)->dict:
            return TokenCtrlMicrosoft.ClientInfo._default
