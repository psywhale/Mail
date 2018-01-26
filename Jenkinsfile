node {
    stage('Cleanup') {
        step([$class: 'WsCleanup'])
    }
    stage('Checkout SCM') {
        checkout scm
    }
    def pythonImage
    stage('build docker image') {

        pythonImage = docker.build("maxsum:build")
    }
    stage('test') {

        slackSend "Build Started - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
        pythonImage.inside {
           sh '. /tmp/venv/bin/activate && python manage.py jenkins --enable-coverage'
        }

    }


    stage('collect test results') {
        junit 'reports/junit.xml'
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