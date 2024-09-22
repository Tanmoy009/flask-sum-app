pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-sum-app'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Tanmoy009/flask-sum-app.git'
            }
        }

        stage('Set up Python Environment') {
            steps {
                sh '''
                python3.11 -m venv myenv
                source myenv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                source myenv/bin/activate
                pytest test_app.py --disable-warnings
                '''
            }
        }

        stage('Build Docker Image') {
            when {
                // Only build Docker image if the tests pass
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                // Build Docker image
                script {
                    docker.build("${IMAGE_NAME}")
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
                // Run the Docker container
                sh """
                docker run -d -p 5000:5000 ${IMAGE_NAME}
                """
            }
        }
    }

    post {
        always {
            // Clean up virtual environment
            sh 'rm -rf myenv'
        }
        success {
            echo 'Pipeline succeeded! Unit tests passed and Docker container created.'
        }
        failure {
            echo 'Pipeline failed! Check the logs for details.'
        }
    }
}