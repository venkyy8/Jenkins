import requests
from requests.auth import HTTPBasicAuth
import csv
import os
from datetime import datetime

# Jenkins Configuration
JENKINS_URL = "http://43.205.236.88:8080"
USERNAME = "admin"
API_TOKEN = "11e261addeb391a613e8b86994fdec9171"

# Output file path
CSV_FILE_PATH = "/opt/jenkins_job_report.csv"

# Disable SSL warnings (only if you're using self-signed certs)
requests.packages.urllib3.disable_warnings()

# Get all jobs
def get_all_jobs():
    url = f"{JENKINS_URL}/api/json"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN), verify=False)
    response.raise_for_status()
    jobs = response.json().get("jobs", [])
    return [job["name"] for job in jobs]

# Get details of the last build
def get_last_build_info(job_name):
    try:
        job_url = f"{JENKINS_URL}/job/{job_name}/api/json"
        job_resp = requests.get(job_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN), verify=False)
        job_resp.raise_for_status()
        last_build = job_resp.json().get("lastBuild")

        if not last_build:
            return None  # No builds for this job

        build_url = last_build["url"] + "api/json"
        build_resp = requests.get(build_url, auth=HTTPBasicAuth(USERNAME, API_TOKEN), verify=False)
        build_resp.raise_for_status()
        build_data = build_resp.json()

        build_number = build_data.get("number", "N/A")
        result = build_data.get("result", "IN PROGRESS")
        timestamp = build_data.get("timestamp", 0)
        triggered_by = "SYSTEM"

        # Convert timestamp to readable time
        build_time = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

        # Check who triggered the job
        actions = build_data.get("actions", [])
        for action in actions:
            if "causes" in action:
                for cause in action["causes"]:
                    if "userName" in cause:
                        triggered_by = cause["userName"]
                    elif "shortDescription" in cause:
                        triggered_by = cause["shortDescription"]

        return {
            "job_name": job_name,
            "build_number": build_number,
            "result": result,
            "timestamp": build_time,
            "triggered_by": triggered_by
        }

    except Exception as e:
        print(f"Error fetching data for job '{job_name}': {e}")
        return None

def write_to_csv(rows, file_path):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Job Name", "Build Number", "Status", "Time", "Triggered By"])
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "Job Name": row["job_name"],
                "Build Number": row["build_number"],
                "Status": row["result"],
                "Time": row["timestamp"],
                "Triggered By": row["triggered_by"]
            })
    print(f"CSV file saved to: {file_path}")

def main():
    try:
        jobs = get_all_jobs()
        job_data = []

        for job in jobs:
            info = get_last_build_info(job)
            if info:
                job_data.append(info)

        if job_data:
            write_to_csv(job_data, CSV_FILE_PATH)
        else:
            print("No job data found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
