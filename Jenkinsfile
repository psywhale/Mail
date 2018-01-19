pipeline {
    agent {
        docker {
            image 'django'
        }
    }
    stages {
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