pipeline {
    agent any

    parameters {
        string(name: 'CI_BUILD_STATUS', defaultValue: 'failed', description: 'Status of the CI job')
    }

    stages {
        stage('Deploy to Staging') {
            when {
                expression { return params.CI_BUILD_STATUS == 'success' }
            }
            steps {
                echo "Proceeding to deploy to staging environment."
                echo "Deploying application to staging..."
            }
        }
    }
    
    post {
        success {
            echo "Deployment job completed successfully!"
        }
        failure {
            echo "Deployment job failed!"
        }
    }
}


