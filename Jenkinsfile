

pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Downloading project from GitHub'
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                bat 'py -3.12 -m venv .venv'
                bat '.venv\\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
    steps {
        bat '''
        set "PYTHONPATH=%WORKSPACE%\\application"
        .venv\\Scripts\\python.exe -m pytest application\\tests -v
        '''
    }
}
}

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t employee-management-app:jenkins-%BUILD_NUMBER% .'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Tests passed and Docker image built!'
        }

        failure {
            echo 'FAILED: Check the Jenkins console output.'
        }
    }
}
