import requests
from requests.auth import HTTPBasicAuth

# CONFIGURATION
JENKINS_URL = "http://43.205.236.88:8080"
USERNAME = "admin"
API_TOKEN = "11e261addeb391a613e8b86994fdec9171"
JOB_NAME = "CI_Job"

def get_last_build_number():
    url = f"{JENKINS_URL}/job/{JOB_NAME}/api/json"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))
    response.raise_for_status()
    data = response.json()
    last_build = data.get('lastBuild')
    if last_build is None:
        raise ValueError("No builds found for this job.")
    return last_build['number']

def get_build_status(build_number):
    url = f"{JENKINS_URL}/job/{JOB_NAME}/{build_number}/api/json"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))
    response.raise_for_status()
    data = response.json()
    # status can be SUCCESS, FAILURE, null (if running)
    return data.get('result')

def main():
    try:
        build_number = get_last_build_number()
        status = get_build_status(build_number)
        print(f"Job Name: {JOB_NAME}")
        print(f"Last Build Number: {build_number}")
        print(f"Status: {status}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
