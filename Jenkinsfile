pipeline {
    agent none
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
            agent {dockerfile true}
            steps {
               checkout scm
               sh 'python manage.py jenkins --enable-coverage'
               }
        }

        stage('Test') {
            agent {dockerfile true}
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