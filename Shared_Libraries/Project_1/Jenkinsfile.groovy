@Library('my-shared-library') _

pipeline {
    agent any

    stages {
        stage('1st Stage') {
            steps {
                helloWorld()
            }
        }
        stage('2nd Stage') {
            steps {
                mavenBuild()
            }
        }
    }
}
