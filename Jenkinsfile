node {
    checkout scm

    def mypython = docker.build("mypython")

    docker.image('mysql:5').withRun('-e "MYSQL_ROOT_PASSWORD=jenkinstest" -e "MYSQL_DATABASE=mail2" ') { c ->
        docker.image('mysql:5').inside("--link ${c.id}:db") {
            /* Wait until mysql service is up */
            sh 'while ! mysqladmin ping -hdb --silent; do sleep 1; done'


        }
        mypython.inside("--link ${c.id}:db") {


            stage('Build') {
                try {
                    sh 'mv jenkinsdb.cnf db.cnf'
                    sh 'mv Mail2proj/settings-jenkins.py Mail2proj/settings.py'
                    sh 'python manage.py makemigrations'
                    sh 'python manage.py migrate'
                 }
                catch(err) {
                    currentBuild.result = 'FAILURE'
                }


               //slackSend "Build started - ${env.JOB_NAME} ${env.BUILD_NUMBER}"

            }
            stage('Test') {
                try {
                    sh 'python manage.py jenkins -v3 --noinput --enable-coverage'
                }
                catch(err){
                    currentBuild.result = 'FAILURE'
                }




            }

            stage('Reports') {
                junit 'reports/junit.xml'
                cobertura autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: 'reports/coverage.xml', conditionalCoverageTargets: '70, 0, 0', failUnhealthy: false, failUnstable: false, lineCoverageTargets: '80, 0, 0', maxNumberOfBuilds: 0, methodCoverageTargets: '80, 0, 0', onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: true
                if (currentBuild == 'FAILURE') {
                    slackSend color:"error",message:"Build FAILED- ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"
                }
                else {
                    slackSend color:"good",message:"Build SUCCESS- ${env.JOB_NAME} ${env.BUILD_NUMBER} (<${env.BUILD_URL}|Open>)"

                }

            }

            }
    }


}