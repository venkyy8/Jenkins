import requests
from requests.auth import HTTPBasicAuth

# Jenkins Configuration
JENKINS_URL = "http://43.205.236.88:8080"
USERNAME = "admin"
API_TOKEN = "11e261addeb391a613e8b86994fdec9171"
JOB_NAME = "CI_Job"

# Disable warnings for self-signed certs (optional)
requests.packages.urllib3.disable_warnings()

def get_all_builds():
    url = f"{JENKINS_URL}/job/{JOB_NAME}/api/json?tree=builds[number,url]"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN), verify=False)
    response.raise_for_status()
    builds = response.json().get("builds", [])
    return builds

def delete_build(build_number):
    url = f"{JENKINS_URL}/job/{JOB_NAME}/{build_number}/doDelete"
    response = requests.post(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN), verify=False)
    if response.status_code == 200:
        print(f"✅ Deleted build #{build_number}")
    elif response.status_code == 302:
        print(f"✅ Deleted build #{build_number} (redirected)")
    else:
        print(f"⚠️ Failed to delete build #{build_number}: HTTP {response.status_code}")

def cleanup_old_builds():
    builds = get_all_builds()

    if len(builds) <= 1:
        print("Nothing to delete — only one or zero builds exist.")
        return

    # Sort builds descending by build number
    sorted_builds = sorted(builds, key=lambda x: x['number'], reverse=True)

    # Keep the most recent build
    builds_to_delete = sorted_builds[1:]

    print(f"🧹 Cleaning up {len(builds_to_delete)} old builds...")

    for build in builds_to_delete:
        delete_build(build['number'])

if __name__ == "__main__":
    cleanup_old_builds()
