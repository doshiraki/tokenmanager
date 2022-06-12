# Token Manager
### ■用途
OAuth2のトークンの取得
- Authorization code方式のため、ユーザを後から紐付けることができる。
- Token取得時に期限が切れている場合、Refreshを行う


## ■使い方
#### 【補足】
- 各例では、Oauth2のクライアント情報のclient_id・client_secretのファイルは「？？_cs.yaml」で
プログラムの初期設定として保存。
- ユーザ情報のaccess_token・refresh_tokenのファイルは「？？_user.yaml」で初回作成されます。
- 時間が期限切れになるとユーザ情報は再作成せれます。

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
※google_user.yaml は初回実行時に認証後、コードを入力することで作成される。

- google_cs.yaml
```yaml
token_ctrl: tokenctrlgoogle.TokenCtrlGoogle
auth_uri: https://accounts.google.com/o/oauth2/auth
token_uri: https://oauth2.googleapis.com/token
client_id: xxx
client_secret: yyy
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


### ◎Atlassianの場合

- Atlassianのトークン取得 
```python
#クライアント情報を元にインスタンス生成
tm = TokenManager("atlassian_cs.yaml", [
    'read:me',
    'read:account',
    'read:confluence-content.summary',
    'read:content:confluence',
    'read:content-details:confluence'
], "atlassian_user.yaml")


#トークンの取得
print(tm.getAccessToken())
```

- atlassian_cs.yaml
```yaml
token_ctrl: tokenctrlatlassian.TokenCtrlAtlassian
auth_uri: https://auth.atlassian.com/authorize
token_uri: https://auth.atlassian.com/oauth/token
client_id: xxx
client_secret: yyy
redirect_uris:
 - "http://localhost"
```
