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

               }
        }

        stage('Test') {

            steps {
                sh 'python manage.py jenkins --enable-coverage'


            }
        }

    }


    post{
        always {
            junit 'reports/junit.xml'
            cobertura autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: 'reports/coverage.xml', conditionalCoverageTargets: '70, 0, 0', failUnhealthy: false, failUnstable: false, lineCoverageTargets: '80, 0, 0', maxNumberOfBuilds: 0, methodCoverageTargets: '80, 0, 0', onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: true
        }

        success {
            slackSend color:"good",message:"Build SUCCESS- ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
        }
        failure {
            slackSend color:"error",message:"Build FAILED- ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
            emailext attachLog: true, body: 'BUILD FAILED', recipientProviders: [[$class: 'CulpritsRecipientProvider']], subject: 'Build Fails'
        }

    }



}