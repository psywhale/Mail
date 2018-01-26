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
        try {
               slackSend "Build Started - ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
               pythonImage.inside {
                    sh '. /tmp/venv/bin/activate && python manage.py jenkins --enable-coverage'
                    }
            } catch(err) {
                slackSend color:"error", message:"${err}"
            }

        }


    stage('collect test results') {
        junit 'reports/junit.xml'
    }



}