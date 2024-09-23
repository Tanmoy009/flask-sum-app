pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-sum-app'
    }

    stages {
        stage('Clone Repository') {
            steps {
                dir('flask-sum-app') {
                    checkout scm
                    git 'https://github.com/Tanmoy009/flask-sum-app.git'
                }
            }
        }

        stage('Set up Python Environment') {
            steps {
                withEnv(['VIRTUAL_ENV=myenv1']) {
                    sh '''
                    python3.11 -m venv myenv1 || { echo "Failed to create virtual environment"; exit 1; }
                    pip install --upgrade pip  # Upgrade pip for compatibility
                    pip install -r requirements.txt || { echo "Failed to install requirements"; exit 1; }
                    '''
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                withEnv(['VIRTUAL_ENV=myenv1']) {
                    sh '''
                    pytest test_app.py --disable-warnings || { echo "Unit tests failed"; exit 1; }
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                script {
                    docker.build(file: 'Dockerfile', tag: "${IMAGE_NAME}") || { echo "Docker build failed"; exit 1; }
                }
            }
        }

        stage('Run Docker Container') {
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                script {
                    def container = docker.run("-d -p 5000:5000 --name ${IMAGE_NAME}_container ${IMAGE_NAME}") || { echo "Failed to run Docker container"; exit 1; }
                    container.id
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up environment...'
            sh '''
            rm -rf myenv1
            docker stop ${IMAGE_NAME}_container || echo "No running container to stop"
            docker rm ${IMAGE_NAME}_container || echo "No container to remove"
            '''
        }
        success {
            echo 'Pipeline succeeded! Unit tests passed and Docker container created.'
        }
        failure {
            echo 'Pipeline failed! Check the logs for details.'
        }
    }
}