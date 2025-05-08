import http.client
from db.config import CLIENT_ID, CLIENT_SECRET
import json

conn = http.client.HTTPSConnection("api.sirv.com")

def get_token():
    """
    Get the token from the API.
    """
    payload = json.dumps({
        "clientId": CLIENT_ID,
        "clientSecret": CLIENT_SECRET
    })

    headers = {
        'content-type': "application/json"
    }

    try:
        conn.request("POST", "/v2/token", payload, headers)
        res = conn.getresponse()
        data = res.read()

        # Parse the JSON response
        result = json.loads(data.decode("utf-8"))

        # Ensure the required fields are present
        if "token" in result and "expiresIn" in result:
            return result["token"], result["expiresIn"]
        else:
            raise ValueError("Invalid response: 'token' or 'expiresIn' not found in the response.")

    except Exception as e:
        print(f"Error while fetching token: {e}")
        return None, None
    
def upload_file(file_path):
    """
    Upload a file to the Sirv server.

    Args:
        file_path (str): The local file path of the ticket.

    Returns:
        bool: True if the upload was successful, False otherwise.
    """
    token, expires_in = get_token()
    if not token:
        print("Failed to get token.")
        return False

    # Extract the filename from the file path
    import os
    filename = os.path.basename(file_path)
    folder_name = "summit_25"
    encoded_filename = f"/{folder_name}/{filename}".replace(" ", "%20")  # URL-encode the filename

    headers = {
        'Content-Type': "application/octet-stream",
        'Authorization': f"Bearer {token}"
    }

    try:
        with open(file_path, "rb") as file:
            # Send the file data in the request body
            conn.request("POST", f"/v2/files/upload?filename={encoded_filename}", file, headers)
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                print(f"File uploaded successfully: {filename}")
                return True
            else:
                print(f"Failed to upload file: {res.status}")
                return False
    except Exception as e:
        print(f"Error while uploading file: {e}")
        return False