# Token Manager
### ■用途
OAuth2のトークンの取得
- Authorization code方式のため、ユーザを後から紐付けることができる。
- Token取得時に期限が切れている場合、Refreshを行う

## ■使い方
### ◎googleの場合
- googleのトークン取得 
```python
#クライアント情報を元にインスタンス生成
tm = TokenManager("google_cs.yaml",
  ['openid', 'https://mail.google.com/'],
  "google_user.yaml")

#トークンの取得
print(tm.getAccessToken())
```

- google_cs.yaml
```yaml
token_ctrl: tokenctrlgoogle.TokenCtrlGoogle
auth_uri: https://accounts.google.com/o/oauth2/auth
token_uri: https://oauth2.googleapis.com/token
client_id: xxx
client_secret: yyy
project_id: zzz
redirect_uris:
 - "http://localhost"
```

- googleのトークン取得 
```python
#クライアント情報を元にインスタンス生成
tm = TokenManager("cs.yaml",
  ['openid', 'https://mail.google.com/'],
  "google_user.yaml")

#トークンの取得
print(tm.getAccessToken())
```
※google_user.yamlは自動生成される。

- google_cs.yaml
```yaml
token_ctrl: tokenctrlgoogle.TokenCtrlGoogle
auth_uri: https://accounts.google.com/o/oauth2/auth
token_uri: https://oauth2.googleapis.com/token
client_id: xxx
client_secret: yyy
project_id: zzz
redirect_uris:
 - "http://localhost"
```

### ◎microsoftの場合

- Microsoftのトークン取得 
```python
#クライアント情報を元にインスタンス生成
tm = TokenManager("microsoft_cs.yaml", [
    'https://graph.microsoft.com/offline_access',
    'https://graph.microsoft.com/email',
    'https://graph.microsoft.com/openid',
    'https://graph.microsoft.com/profile',
    'https://graph.microsoft.com/IMAP.AccessAsUser.All'], "microsoft_user.yaml")


#トークンの取得
print(tm.getAccessToken())
```

- microsoft_cs.yaml
```yaml
token_ctrl: tokenctrlmicrosoft.TokenCtrlMicrosoft
auth_uri: https://login.microsoftonline.com/(tenant id)
client_id: (application id)
client_secret: (secret)
redirect_uris:
 - https://login.microsoftonline.com/common/oauth2/nativeclient
```
