pipeline {
    agent {
        docker {
            image 'django'
        }
    }
    stages {
        stage('Setup') {
            steps {
                echo "setup"
            }
        }
        stage('Test') {
            steps {
                sh 'sudo -H pip install -r requirements.txt'
                sh 'python manage.py test'
            }
        }
    }
}