#!/bin/bash

# Set variables
JENKINS_HOME="/var/lib/jenkins"            # Path to Jenkins home directory
BACKUP_DIR="/tmp/jenkins-backup"           # Temporary backup directory
S3_BUCKET="s3://bucket-for-backup-venkat-data/backups"  # S3 bucket path
DATE=$(date +'%Y-%m-%d_%H-%M-%S')          # Date format for backup file name
BACKUP_FILE="jenkins_backup_$DATE.tar.gz"  # Backup file name

# Step 1: Create a temporary backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Step 2: Backup Jenkins home directory
echo "Starting backup of Jenkins home directory..."
tar -czf $BACKUP_DIR/$BACKUP_FILE -C $JENKINS_HOME .

# Step 3: Upload the backup to the S3 bucket
echo "Uploading backup to S3 bucket..."
aws s3 cp $BACKUP_DIR/$BACKUP_FILE $S3_BUCKET/

# Step 4: Clean up local backup file
echo "Cleaning up local backup..."
rm -f $BACKUP_DIR/$BACKUP_FILE

# Step 5: Optional - Delete old backups from S3 (older than 30 days)
echo "Deleting old backups from S3..."
aws s3 ls $S3_BUCKET/ | grep 'jenkins_backup_' | while read -r line; do
    # Extract the date of the backup
    backup_date=$(echo $line | awk '{print $1}')
    backup_epoch=$(date -d $backup_date +%s)
    cutoff_date=$(date -d '30 days ago' +%s)

    # Delete if older than 30 days
    if [ $backup_epoch -lt $cutoff_date ]; then
        backup_filename=$(echo $line | awk '{print $4}')
        echo "Deleting old backup: $backup_filename"
        aws s3 rm "$S3_BUCKET/$backup_filename"
    fi
done

# Step 6: Final message
echo "Backup completed and old backups cleaned up (if any)."
