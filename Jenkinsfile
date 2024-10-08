pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-sum-app'
        VIRTUAL_ENV = 'myenvnew'
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
                chmod +x /var/snap/jenkins/4742/workspace/flask-test/myenvnew/bin/activate*
                chmod +x /var/snap/jenkins/4742/workspace/flask-test/myenvnew/bin/Activate*
                ./${VIRTUAL_ENV}/bin/activate || { echo "failed to activate"; exit 1; }
                /var/snap/jenkins/4742/workspace/flask-test/myenvnew/bin/pip install --upgrade pip
                /var/snap/jenkins/4742/workspace/flask-test/myenvnew/bin/pip install -r requirements.txt || { echo "Failed to install requirements"; exit 1; }

                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                ./${VIRTUAL_ENV}/bin/activate || { echo "failed to activate"; exit 1; }
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
                
                sh '''
                docker build -t ${IMAGE_NAME} . || { echo "Docker build failed"; exit 1; }
                '''
                
            }
        }

        stage('Run Docker Container') {
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                    sh '''
                    docker run -d -p 5000:5000 ${IMAGE_NAME} || { echo "Docker run failed"; exit 1; }
                    '''         
        }
    }
    }

    post {
        always {
            echo 'Cleaning up environment...'
            sh '''
            #rm -rf ${VIRTUAL_ENV}
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