import requests
import json
import base64
import time
import os

class IdealistaAPIClient:
    def __init__(self, client_id, client_secret, feed_key, sandbox=True):
        self.client_id = client_id
        self.client_secret = client_secret
        self.feed_key = feed_key
        self.base_url = "https://partners-sandbox.idealista.com/v1" if sandbox else "https://partners.idealista.com/v1"
        self.auth_url = "https://partners-sandbox.idealista.com/oauth/token" if sandbox else "https://partners.idealista.com/oauth/token"
        self.token = None
        self.token_expiry = 0

    def _get_auth_header(self):
        """Generates the Basic Auth header for token requests."""
        # Note: URL encoding for ID and SECRET if they contain special chars
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
        }

    def authenticate(self):
        """Requests a new access token using client_credentials grant."""
        headers = self._get_auth_header()
        data = {
            "grant_type": "client_credentials",
            "scope": "read write"
        }
        
        response = requests.post(self.auth_url, headers=headers, data=data)
        
        if response.status_code == 200:
            res_json = response.json()
            self.token = res_json.get("access_token")
            # Set expiry with a small buffer (5 seconds)
            self.token_expiry = time.time() + res_json.get("expires_in", 0) - 5
            print("Successfully authenticated with Idealista API.")
            return True
        else:
            print(f"Authentication failed: {response.status_code} - {response.text}")
            return False

    def _get_api_headers(self):
        """Standard headers required for every API request."""
        if not self.token or time.time() >= self.token_expiry:
            self.authenticate()
            
        return {
            "Authorization": f"Bearer {self.token}",
            "feedKey": self.feed_key,
            "Content-Type": "application/json"
        }

    def publish_property(self, property_data):
        """Publishes a new property (POST /properties)."""
        url = f"{self.base_url}/properties"
        headers = self._get_api_headers()
        
        response = requests.post(url, headers=headers, json=property_data)
        return response.json() if response.status_code in [200, 201] else response.text

    def update_property(self, property_id, property_data):
        """Updates an existing property (PUT /properties/{id})."""
        url = f"{self.base_url}/properties/{property_id}"
        headers = self._get_api_headers()
        
        response = requests.put(url, headers=headers, json=property_data)
        return response.json() if response.status_code == 200 else response.text

    def delete_property(self, property_id):
        """Deletes a property listing (DELETE /properties/{id})."""
        url = f"{self.base_url}/properties/{property_id}"
        headers = self._get_api_headers()
        
        response = requests.delete(url, headers=headers)
        return response.status_code == 204

    def update_images(self, property_id, images_list):
        """Updates images for a property (PUT /properties/{id}/images)."""
        # This replaces the entire image set for the property.
        url = f"{self.base_url}/properties/{property_id}/images"
        headers = self._get_api_headers()
        
        response = requests.put(url, headers=headers, json=images_list)
        return response.json() if response.status_code == 200 else response.text

if __name__ == "__main__":
    # Test credentials from the Idealista email (Sandbox)
    # The actual API credentials (API SECRET) will be requested via the draft email.
    # For now, we use the ones provided for 'API Reference' if they work for logic tests.
    
    # Note: These are placeholder credentials until the final ones are received.
    CLIENT_ID = "testDocu"
    CLIENT_SECRET = "dc4haw4JmASg2CZG"
    FEED_KEY = "ilc8b226" # Placeholder short version, must be 43 chars for production
    
    client = IdealistaAPIClient(CLIENT_ID, CLIENT_SECRET, FEED_KEY)
    
    # Example logic test (uncomment when real sandbox credentials are ready)
    # client.authenticate()
