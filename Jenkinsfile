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
                dir('backend') {
                    sh 'pip3 install flask flask_sqlalchemy flask_bcrypt email-validator web3 cryptography ipfshttpclient pyjwt'
                }
            }
        }

        stage('Run Backend') {
            steps {
                dir('backend') {
                    sh 'nohup python3 app.py &'
                }
            }
        }
    }
}
