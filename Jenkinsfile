pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Gouthamvaishnav11/AuricDefence.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t auricdefence:latest .'
            }
        }

        stage('Run Docker Container') {
            steps {
                // Stop old container if running
                sh 'docker rm -f auricdefence || true'
                // Run new container
                sh 'docker run -d -p 5000:5000 --name auricdefence auricdefence:latest'
            }
        }
    }
}
