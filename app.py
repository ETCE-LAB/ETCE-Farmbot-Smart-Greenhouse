import requests

# Set your application ID, device ID, and access key
application_id = 'tuc-isse-sensorik'
device_id = 'eui-70b3d57ed005ea4a'  # Replace with your actual device ID
access_key = 'NNSXS.DWWKJ3GCY4SX6SYXOFIHEA2SUMFRC6UQSE7BFFI.YAJWGXZJTYZAXKPE7NJBF6MDPMGH5CNYAZ4XHHBUIETCGFLA4EEA'  # Use an environment variable or secure method to handle this


# Construct the URL for application data
data_type = 'uplink_message'
app_url = f"https://eu1.cloud.thethings.network/api/v3/as/applications/{application_id}/packages/storage/{data_type}"

# Headers for authentication
headers = {
    'Authorization': f'Bearer {access_key}',
    'Accept': '*/*'  # Accept any media type
}

# Perform the GET request
response = requests.get(app_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    try:
        # Try to parse JSON first
        print("Data Retrieved Successfully:")
        print(response.json())
    except ValueError:
        # Fallback if response is not JSON
        print("Received non-JSON response:")
        print(response.text)
else:
    print("Failed to retrieve data:", response.status_code, response.text)

# Construct the URL for device-specific data and make a request
device_url = f"https://eu1.cloud.thethings.network/api/v3/as/applications/{application_id}/devices/{device_id}/packages/storage/{data_type}"
device_response = requests.get(device_url, headers=headers)

if device_response.status_code == 200:
    try:
        print("Device Data Retrieved Successfully:")
        print(device_response.json())
    except ValueError:
        print("Received non-JSON response:")
        print(device_response.text)
else:
    print("Failed to retrieve device data:", device_response.status_code, device_response.text)
