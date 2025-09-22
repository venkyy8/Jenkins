import requests
from requests.auth import HTTPBasicAuth

# Jenkins configuration
JENKINS_URL = "http://43.205.236.88:8080"
USERNAME = "admin"
API_TOKEN = "11e261addeb391a613e8b86994fdec9171"
JOB_NAME = "CI_Job"

def trigger_jenkins_job():
    # URL to trigger the build
    build_url = f"{JENKINS_URL}/job/{JOB_NAME}/build"

    try:
        response = requests.post(build_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

        if response.status_code == 201:
            print(f"✅ Job '{JOB_NAME}' triggered successfully.")
        elif response.status_code == 403:
            print("❌ Authentication failed (403). Check your credentials or API token.")
        elif response.status_code == 404:
            print(f"❌ Job '{JOB_NAME}' not found.")
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"❌ Error triggering job: {e}")

if __name__ == "__main__":
    trigger_jenkins_job()
