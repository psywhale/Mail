pipeline {
    agent none
    stages {

        stage('Build') {
            agent {dockerfile true}
            steps {
               checkout scm
               sh 'python manage.py jenkins --enable-coverage'
               }
        }

        stage('test') {
            steps {
                pwd

            }

        }


    }


    post{
        always {
            junit 'reports/junit.xml'
        }
        success {
            slackSend color:"good",message:"Build SUCCESS- ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
        }
        failure {
            slackSend color:"error",message:"Build FAILED- ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
        }

    }



}