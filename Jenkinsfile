node {

    docker.image('mysql:5').withRun('-e "MYSQL_ROOT_PASSWORD=jenkinstest" -e "MYSQL_DATABASE=mail2" ') { c ->
        docker.image('mysql:5').inside("--link ${c.id}:db") {
            /* Wait until mysql service is up */
            sh 'while ! mysqladmin ping -hdb --silent; do sleep 1; done'


        }
        docker.image('ubuntu:xenial').inside("--link ${c.id}:db") {

            stage('Build') {

               //slackSend "Build started - ${env.JOB_NAME} ${env.BUILD_NUMBER}"
               checkout scm

               sh 'apt-get update'
               sh 'apt-get upgrade -y'
               sh 'apt-get -y install python3-dev pip3 virtualenv'
               sh 'pip3 install --upgrade pip'
               sh 'virtualenv -p python3.5 /tmp/venv'
               sh 'source /tmp/venv/bin/activate'
               sh 'pip install --no-cache-dir -r requirements.txt'
               sh 'deactivate'


            }
            stage('Test') {
                sh 'whoami'


                sh 'mv jenkinsdb.cnf db.cnf'
                sh 'source /tmp/venv/bin/activate'
                sh 'python manage.py jenkins --noinput --enable-coverage'
                sh 'deactivate'

                }

            }
    }



/*
    post {
        always {
            junit 'reports/junit.xml'
            cobertura autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: 'reports/coverage.xml', conditionalCoverageTargets: '70, 0, 0', failUnhealthy: false, failUnstable: false, lineCoverageTargets: '80, 0, 0', maxNumberOfBuilds: 0, methodCoverageTargets: '80, 0, 0', onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: true
        }

        success {
            slackSend color:"good",message:"Build SUCCESS- ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
        }
        failure {
            //slackSend color:"error",message:"Build FAILED- ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
            emailext attachLog: true, body: 'BUILD FAILED', recipientProviders: [[$class: 'CulpritsRecipientProvider']], subject: 'Build Fails'
        }

    }
*/


}