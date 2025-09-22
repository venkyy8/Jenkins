import os
import tarfile
import boto3
import time
from datetime import datetime

# Constants
JENKINS_HOME = "/var/lib/jenkins"  # Path to Jenkins home directory
BACKUP_DIR = "/tmp/jenkins-backup"  # Temporary backup directory
S3_BUCKET = "bucket-for-backup-venkat-data"      # S3 bucket name (replace with your bucket name)

# Get the current date and time for the backup file name
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
BACKUP_FILE = f"jenkins_backup_{current_time}.tar.gz"  # Backup file name

# Step 1: Create temporary backup directory if it doesn't exist
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Step 2: Create a tarball backup of the Jenkins home directory
def create_backup():
    backup_file_path = os.path.join(BACKUP_DIR, BACKUP_FILE)
    print(f"Creating backup of Jenkins home directory at {backup_file_path}...")

    with tarfile.open(backup_file_path, "w:gz") as tar:
        tar.add(JENKINS_HOME, arcname=os.path.basename(JENKINS_HOME))

    return backup_file_path

# Step 3: Upload the backup to S3
def upload_to_s3(backup_file_path):
    print(f"Uploading backup to S3 bucket: {S3_BUCKET}...")

    s3 = boto3.client('s3')
    try:
        s3.upload_file(backup_file_path, S3_BUCKET, f"backups/{BACKUP_FILE}")
        print(f"Backup uploaded successfully: s3://{S3_BUCKET}/backups/{BACKUP_FILE}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

# Step 4: Clean up the local backup file
def cleanup_local_backup(backup_file_path):
    print("Cleaning up local backup...")
    if os.path.exists(backup_file_path):
        os.remove(backup_file_path)
        print(f"Local backup {backup_file_path} removed.")

# Step 5: Optional - Delete backups older than 30 days from S3
def delete_old_backups_from_s3():
    print("Deleting old backups from S3 bucket...")
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix='backups/')

    if 'Contents' in response:
        for obj in response['Contents']:
            backup_file = obj['Key']
            last_modified = obj['LastModified']

            # Calculate the age of the backup
            backup_age = (datetime.now() - last_modified.replace(tzinfo=None)).days

            # If backup is older than 30 days, delete it
            if backup_age > 30:
                print(f"Deleting backup {backup_file} (Age: {backup_age} days)...")
                s3.delete_object(Bucket=S3_BUCKET, Key=backup_file)
                print(f"Backup {backup_file} deleted from S3.")

# Main execution
def main():
    # Create the backup
    backup_file_path = create_backup()

    # Upload the backup to S3
    upload_to_s3(backup_file_path)

    # Clean up the local backup
    cleanup_local_backup(backup_file_path)

    # Optionally, delete old backups from S3
    delete_old_backups_from_s3()

    print("Backup process completed successfully.")

if __name__ == "__main__":
    main()
