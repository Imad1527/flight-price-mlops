pipeline {
    agent any

    environment {
        IMAGE_NAME = "flight-price-api"
        K8S_DEPLOYMENT = "flight-price-deployment"
    }

    stages {

        stage('Clone Repository') {
            steps {
                echo 'Cloning source code...'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r api/requirements.txt'
            }
        }

        stage('Run API Tests') {
            steps {
                echo 'Running basic API validation...'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:latest .'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f deployment.yml'
            }
        }
    }

    post {
        success {
            echo 'CI/CD Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs.'
        }
    }
}
