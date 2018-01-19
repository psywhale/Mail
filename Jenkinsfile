pipeline {
    agent {
        docker {
            image 'django'
        }
    }
    stages {
        stage('Setup') {
            steps {


            }
        }
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python manage.py test'
            }
        }
    }
}