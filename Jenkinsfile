pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Gouthamvaishnav11/AuricDefence.git'
            }
        }

        stage('Install Backend Dependencies') {
            steps {
                sh '''
                   pip3 install --upgrade pip
                   pip3 install flask flask_sqlalchemy flask_bcrypt email-validator web3 cryptography ipfshttpclient pyjwt python-dotenv
                '''
            }
        } 

        stage('Run Backend') {
            steps {
                sh 'nohup python3 app.py &'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t auricdefence-backend .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d -p 5000:5000 auricdefence-backend'
            }
        }
    }
}
