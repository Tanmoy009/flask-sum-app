pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-sum-app'
        VIRTUAL_ENV = 'myenv-new'
    }

    stages {
        stage('Clone Repository') {
            steps {
                dir('flask-sum-app') {
                    checkout scm  // Only using checkout scm
                }
            }
        }

        stage('Set up Python Environment') {
            steps {
                sh '''
                python3.11 -m venv ${VIRTUAL_ENV} || { echo "Failed to create virtual environment"; exit 1; }
                cd /var/snap/jenkins/4742/workspace/flask-test
                source ${VIRTUAL_ENV}/bin/activate || { echo "failed to activate"; exit 1; }
                pip install pip  
                pip install -r requirements.txt || { echo "Failed to install requirements"; exit 1; }

                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                source ${VIRTUAL_ENV}/bin/activate
                pytest test_app.py --disable-warnings || { echo "Unit tests failed"; exit 1; }
                '''
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
                    docker.build("${IMAGE_NAME}", ".")  // Removed error handling here
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
                    def container = docker.run("-d -p 5000:5000 --name ${IMAGE_NAME}_container ${IMAGE_NAME}")
                    container.id
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up environment...'
            sh '''
            rm -rf ${VIRTUAL_ENV}
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