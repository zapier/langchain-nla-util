import requests
from requests_oauthlib import OAuth2Session

class OAuthHandler:
    def __init__(self, client_id, client_secret, redirect_uri, authorization_base_url, token_url, scope=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authorization_base_url = authorization_base_url
        self.token_url = token_url
        self.scope = scope

        self.oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, scope=self.scope)

    def authorization_url(self):
        return self.oauth.authorization_url(self.authorization_base_url)

    def fetch_token(self, authorization_response):
        return self.oauth.fetch_token(self.token_url, client_secret=self.client_secret, authorization_response=authorization_response)

    def refresh_token(self, refresh_token):
        extra = {'client_id': self.client_id, 'client_secret': self.client_secret}
        return self.oauth.refresh_token(self.token_url, refresh_token=refresh_token, **extra)

    def request(self, method, url, **kwargs):
        response = self.oauth.request(method, url, **kwargs)

        if response.status_code == 401:
            token = self.refresh_token(self.oauth.token['refresh_token'])
            self.oauth.token = token
            response = self.oauth.request(method, url, **kwargs)

        return response
