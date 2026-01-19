pipeline {
    agent any

    stages {
        stage('Verify Environment') {
            steps {
                echo 'Jenkins pipeline started'
                bat 'docker --version'
                bat 'kubectl version --client'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies'
                bat 'python --version'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'
                bat 'docker build -t flight-price-api:latest .'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes'
                bat 'kubectl apply -f k8s/'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully'
        }
        failure {
            echo 'Pipeline failed. Check logs.'
        }
    }
}
