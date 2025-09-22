#!/bin/bash

# CONFIGURATION
JENKINS_URL="http://43.205.236.88:8080"
USERNAME="admin"
API_TOKEN="11e261addeb391a613e8b86994fdec9171"
JOB_NAME="CI_Job"

# Get the last build number
BUILD_NUMBER=$(curl -s -u $USERNAME:$API_TOKEN "$JENKINS_URL/job/$JOB_NAME/api/json" | jq '.lastBuild.number')

# Check if build number was retrieved
if [ -z "$BUILD_NUMBER" ]; then
  echo "Failed to get last build number. Please check job name or credentials."
  exit 1
fi

# Get the last build status
BUILD_STATUS=$(curl -s -u $USERNAME:$API_TOKEN "$JENKINS_URL/job/$JOB_NAME/$BUILD_NUMBER/api/json" | jq -r '.result')

# Output the results
echo "Job Name: $JOB_NAME"
echo "Last Build Number: $BUILD_NUMBER"
echo "Status: $BUILD_STATUS"
