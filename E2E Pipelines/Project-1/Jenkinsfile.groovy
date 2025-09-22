pipeline {
    agent any
    tools {
        maven 'maven'
    }
    stages {
        stage('Github') {
            steps {
                git 'https://github.com/MithunTechnologiesDevOps/Springboot-Mongo-Application.git'
            }
        }
        stage('unit test') {
            steps {
                sh "mvn clean test"
            }
        }
        stage('integration test') {
            steps {
                sh "mvn verify -DskipTests=true"
            }
        }
        stage('SonarQube analysis') {
            steps {
                script {
                    withSonarQubeEnv('sonar-jenkins') {
                        sh "mvn sonar:sonar"
                    }
                }
            }
        }
        stage('Build Application') {
            steps {
                sh "mvn package compile install"
            }
        }
        stage('tomcat') {
            steps {
                sshagent(['tomcat-ID']) {
                    sh "scp -o StrictHostKeyChecking=no /var/lib/jenkins/workspace/ci_cd/target/java-web-app*.war ubuntu@3.82.113.172:/opt/tomcat/webapps"
                }
            }
        }
        stage("Publish to Nexus Repository Manager") {
            steps {
                script {
                    nexusArtifactUploader(
                        artifacts: [
                            [artifactId: 'java-web-app', classifier: '', file: '/var/lib/jenkins/workspace/ci_cd/target/java-web-app-1.0.war', type: 'war']
                        ],
                        credentialsId: 'nexus-id',
                        groupId: 'com.mt',
                        nexusUrl: '44.210.144.192:8081',
                        nexusVersion: 'nexus3',
                        protocol: 'http',
                        repository: 'nexus-repo-maven-jenkins',
                        version: "${BUILD_NUMBER}"
                    )
                }
            }
        }
        stage('docker build') {
            steps {
                sh "docker build -t venkyy82/venky:${BUILD_NUMBER} ."
            }
        }
        stage('docker push') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'docker2-id', variable: 'dockerpwd')]) {
                        sh "docker login -u venkyy82 -p ${dockerpwd}"
                        sh "docker push venkyy82/venky:${BUILD_NUMBER}"
                    }
                }
            }
        }
        stage('push to  ecr') {
            steps {
                sh "aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/i4w3s2p5"
                //sh "docker build -t demo-ecr ."
                sh "docker tag venkyy82/venky:${BUILD_NUMBER} public.ecr.aws/i4w3s2p5/demo-ecr:${BUILD_NUMBER}"
                sh "docker push public.ecr.aws/i4w3s2p5/demo-ecr:${BUILD_NUMBER}"
            }
        }
        stage("deploy into Ec2 server"){
            steps{
                sshagent(['secret_key']) {
                        // sh "ssh -o StrictHostKeyChecking=no ubuntu@172.31.14.42 docker rm -f springbootcontainer || true"
                        // sh "ssh -o StrictHostKeyChecking=no ubuntu@172.31.14.42 docker run -d -p 8081:8080 --name springbootcontainer chandandocker1995/springbootapp:1"
                        sh "ssh -o StrictHostKeyChecking=no ubuntu@172.31.14.42 sudo rm -rf /opt/compose || true"
                        sh "ssh -o StrictHostKeyChecking=no ubuntu@172.31.14.42 sudo mkdir /opt/compose"
                        sh "ssh -o StrictHostKeyChecking=no ubuntu@172.31.14.42 sudo chmod 777 /opt/compose"
                        sh "scp -o StrictHostKeyChecking=no /var/lib/jenkins/workspace/spring-boot-application/docker-compose.yml ubuntu@172.31.14.42:/opt/compose/compose.yml"
                        sh '''
                        ssh -o StrictHostKeyChecking=no ubuntu@172.31.14.42 sudo apt-get update
                        ssh -o StrictHostKeyChecking=no ubuntu@172.31.14.42 sudo docker-compose -f /opt/compose/compose.yml down || true
                        ssh -o StrictHostKeyChecking=no ubuntu@172.31.14.42 sudo docker-compose -f /opt/compose/compose.yml up -d
                        '''       
                    }
                
                }
            }
        }
    }
