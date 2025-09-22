pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Executing basic build step...'
            }
        }

        stage('Notify') {
            steps {
                echo 'Preparing email notification...'
            }
        }
    }

    post {
        always {
            script {
                // Safe way to get triggering user
                def triggeredBy = "Unknown"
                def causes = currentBuild.getBuildCauses()
                if (causes.size() > 0 && causes[0].userId) {
                    triggeredBy = causes[0].userName
                }

                def emailBody = """
                Hello,

                This is a Jenkins build notification.

                Job Name: ${env.JOB_NAME}
                Build Number: ${env.BUILD_NUMBER}
                Build Status: ${currentBuild.currentResult}
                Triggered By: ${triggeredBy}
                Build URL: ${env.BUILD_URL}

                Regards,
                Jenkins
                """

                emailext(
                    to: 'venkyy82@gmail.com',
                    from: 'venkyy82@gmail.com',
                    subject: "Build Notification: ${env.JOB_NAME} #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
                    body: emailBody,
                    mimeType: 'text/plain'
                )
            }
        }
    }
}
