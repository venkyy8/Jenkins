
# 🚀 Jenkins CI/CD Pipeline: Conditional Deployment Trigger

This repository contains a basic Jenkins-based CI/CD pipeline demonstrating **conditional job triggering**. The objective is to **trigger a deployment (CD) job only when the CI job completes successfully**.

---

## 🧩 Overview

This setup consists of two Jenkins jobs:

* **CI Job** (`CI_Job`):
  Responsible for building the application. It acts as the entry point to the pipeline.

* **CD Job** (`CD_Job`):
  Handles the deployment process. It is only triggered if the CI job completes successfully.

---

## 🔁 Workflow Summary

1. The pipeline begins with the execution of the **CI job**.
2. If the CI job's build process is **successful**, it triggers the **CD job**, passing a status parameter indicating success.
3. The **CD job** checks the received parameter:

   * If the status is **`success`**, deployment proceeds.
   * If the status is anything else, deployment is skipped.
4. If the **CI job fails**, the **CD job is not triggered at all**.

---

## 🛠️ Setup Instructions

1. Create two Jenkins pipeline jobs:

   * `CI_Job`
   * `CD_Job`

2. Configure each job to use the appropriate pipeline script from this repository.

3. Ensure the `CI_Job` is triggered either manually or via source control integration (e.g., GitHub webhook).

---

## ✅ Key Features

* **Conditional Job Triggering**: CD job is only triggered if the CI job succeeds.
* **Parameter Passing**: CI job passes build status to CD job.
* **Simple and Extendable**: Easy to enhance with notifications, approvals, or environment promotion logic.

---

## 📌 Use Cases

* Controlled deployments after successful builds
* Staging deployments following CI verification
* Clean separation of build and deploy concerns in Jenkins

---

