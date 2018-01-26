pipeline {
    agent {dockerfile true}
    stages {
        stage('Cleanup') {
            steps{cleanWs()}
        }
        stage('Checkout SCM') {
            steps {
               checkout scm
               }
        }

        stage('test') {
            steps {
                sh './python manage.py jenkins --enable-coverage'
            }

        }

        stage('collect test results') {
            steps {
                junit 'reports/junit.xml'
            }

        }
    }


    post{
        success {
            slackSend color:"good",message:"Build SUCCESS- ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
        }
        failure {
            slackSend color:"error",message:"Build FAILED- ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
        }

    }



}