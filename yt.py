import requests
import google_auth_httplib2
import googleapiclient
import oauthlib

#API KEY = AIzaSyDScBi9fDiB_UpFZdpugCdhmWZk7vrr7AY

class DataLoader:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def load_data(self, params):
        # Make API call using self.api_url and self.api_key
        # Return the loaded data
        response = requests.get(self.api_url, params=params)
        return response.json()
    
loader = DataLoader("")