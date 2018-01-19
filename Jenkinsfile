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
                sh 'virtualenv venv'
            }
        }
        stage('Test') {
            steps {
                sh 'source venv/bin/activate'
                sh 'pip install -r requirements.txt'
                sh 'python manage.py test'
            }
        }
    }
}