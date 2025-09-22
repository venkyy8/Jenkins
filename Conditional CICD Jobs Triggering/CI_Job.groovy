pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    echo "Building the project..."
                    
                    // Simulate a build failure by uncommenting the line below
                    //exit 1
                }
            }
        }

        stage('Trigger Deployment (CD) Job') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                script {
                    echo "CI Job succeeded, triggering Deployment (CD) Job..."

                    build job: 'CD_Job',
                        parameters: [
                            string(name: 'CI_BUILD_STATUS', value: 'success')
                        ]
                }
            }
        }
    }

    post {
        success {
            echo "CI Job pipeline completed successfully!"
        }
        failure {
            echo "CI Job pipeline failed. Skipping deployment trigger."
        }
    }
}
