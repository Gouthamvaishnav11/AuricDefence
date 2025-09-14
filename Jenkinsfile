pipeline {
    agent any

    environment {
        BACKEND_DIR = 'backend'
        FLASK_FILE = 'app.py'  // <-- change this if your main file has a different name
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Gouthamvaishnav11/AuricDefence.git'
            }
        }

        stage('Install Backend Dependencies') {
            steps {
                dir("${BACKEND_DIR}") {
                    sh '''
                    echo "Installing backend dependencies..."
                    pip3 install --user flask flask_sqlalchemy flask_bcrypt email-validator web3 cryptography ipfshttpclient pyjwt
                    '''
                }
            }
        }

        stage('Run Backend') {
            steps {
                dir("${BACKEND_DIR}") {
                    sh '''
                    if [ ! -f ${FLASK_FILE} ]; then
                        echo "ERROR: ${FLASK_FILE} not found!"
                        exit 1
                    fi
                    echo "Starting Flask app..."
                    nohup python3 ${FLASK_FILE} > backend.log 2>&1 &
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully. Flask app should be running!"
        }
        failure {
            echo "Pipeline failed. Check the console output for errors."
        }
    }
}
