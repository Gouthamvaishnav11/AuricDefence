pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Gouthamvaishnav11/AuricDefence.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                  echo "Installing dependencies..."
                  cd frontend && npm install
                  cd ../backend && pip install -r requirements.txt
                '''
            }
        }

        stage('Build Frontend') {
            steps {
                sh '''
                  echo "Building frontend..."
                  cd frontend && npm run build
                '''
            }
        }

        stage('Run Backend') {
            steps {
                sh '''
                  echo "Starting backend..."
                  cd backend && nohup python app.py &
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh 'echo "Deployment step goes here (Docker, SSH, or server copy)"'
            }
        }
    }
}
