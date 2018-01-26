pipeline {
    agent {dockerfile true}
    stages {

/*
        stage('Clean') {
            agent {dockerfile true}
            steps {
                deleteDir()
            }
        }
        */

        stage('Build') {

            steps {
               slackSend "Build started - ${env.JOB_NAME} ${env.BUILD_NUMBER}"
               checkout scm
               sh 'pwd'


               sh 'pip install -r requirements.txt'
               sh 'python manage.py jenkins --enable-coverage'
               }
        }

        stage('Test') {

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