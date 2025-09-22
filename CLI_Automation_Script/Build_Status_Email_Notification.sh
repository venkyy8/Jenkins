#!/bin/bash

# CONFIGURATION
JENKINS_URL="http://43.205.236.88:8080"
USERNAME="admin"
API_TOKEN="11e261addeb391a613e8b86994fdec9171"
JOB_NAME="CI_Job"

EMAIL_FROM="venkyy82@gmail.com"
EMAIL_TO="venkyy82@gmail.com"
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="venkyy82@gmail.com"
SMTP_PASS="bjwf ldik azsp cigt"  # Your app password

# Temporary files
TMP_BODY=$(mktemp)
TMP_HDR=$(mktemp)

function cleanup {
  rm -f "$TMP_BODY" "$TMP_HDR"
}
trap cleanup EXIT

# Fetch last build number
BUILD_NUMBER=$(curl -s -u "$USERNAME:$API_TOKEN" "$JENKINS_URL/job/$JOB_NAME/api/json" | jq '.lastBuild.number')

if [ -z "$BUILD_NUMBER" ] || [ "$BUILD_NUMBER" = "null" ]; then
  echo "Failed to get last build number. Check job name or credentials."
  exit 1
fi

# Fetch build status
BUILD_STATUS=$(curl -s -u "$USERNAME:$API_TOKEN" "$JENKINS_URL/job/$JOB_NAME/$BUILD_NUMBER/api/json" | jq -r '.result')

# Compose email content
SUBJECT="Jenkins Build Status for $JOB_NAME"
BODY="Job Name: $JOB_NAME
Last Build Number: $BUILD_NUMBER
Status: $BUILD_STATUS"

echo "$BODY" > "$TMP_BODY"

# Compose email headers
cat <<EOF > "$TMP_HDR"
From: $EMAIL_FROM
To: $EMAIL_TO
Subject: $SUBJECT
EOF

# Send email using msmtp
# You need to have msmtp installed and configured below:

msmtp --host=$SMTP_SERVER --port=$SMTP_PORT --tls=on \
      --auth=on --user=$SMTP_USER --passwordeval="echo $SMTP_PASS" \
      --from=$EMAIL_FROM $EMAIL_TO < <(cat "$TMP_HDR" && echo && cat "$TMP_BODY")

if [ $? -eq 0 ]; then
  echo "Email sent successfully."
else
  echo "Failed to send email."
fi
