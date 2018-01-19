pipeline {
    agent {
        docker {
            image 'django'
        }
    }
    stages {
        stage('Setup') {
            steps {
                sh 'apt-get update'
                sh 'apt-get install -y python3 python3-dev python3-pip virtualenv'
            }
        }
        stage('Test') {
            steps {
                sh 'virtualenv --python=python3 venv'
                sh 'source venv/bin/activate'
                sh 'pip install -r requirements.txt'
                sh 'python manage.py test'
            }
        }
    }
}