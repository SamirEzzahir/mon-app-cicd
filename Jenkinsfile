pipeline {
    agent any

    environment {
        IMAGE_NAME = 'mon-app-cicd'
        CONTAINER_NAME = 'app-running'
        APP_PORT = '5000'
        IMAGE_TAG = "${IMAGE_NAME}:${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Récupération du code depuis GitHub...'
                checkout scm
                echo "✅ Code récupéré — Build n°${BUILD_NUMBER}"
            }
        }

        stage('Build Image Docker') {
            steps {
                echo '🐳 Construction de l image Docker...'
                sh "docker build -t ${IMAGE_TAG} ."
                sh "docker tag ${IMAGE_TAG} ${IMAGE_NAME}:latest"
                echo "✅ Image construite : ${IMAGE_TAG}"
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Smoke test de l application...'
                sh """
                docker run -d --name test-${BUILD_NUMBER} -p 5001:5000 ${IMAGE_TAG}
                sleep 10
                curl -f http://192.168.70.128:5001 || exit 1
                docker stop test-${BUILD_NUMBER}
                docker rm test-${BUILD_NUMBER}
                """
                echo '✅ Test réussi !'
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Déploiement du conteneur...'

                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"

                sh """
                docker run -d \\
                --name ${CONTAINER_NAME} \\
                -p ${APP_PORT}:5000 \\
                -e APP_VERSION=${BUILD_NUMBER} \\
                ${IMAGE_NAME}:latest
                """

                echo "✅ Application disponible sur http://localhost:${APP_PORT}"
            }
        }
    }

    post {
        success {
            echo '''
╔════════════════════════════════════╗
║ ✅ PIPELINE RÉUSSI !              ║
║ Application déployée avec succès  ║
╚════════════════════════════════════╝
'''
        }

        failure {
            echo '❌ PIPELINE ÉCHOUÉ — Consulte les logs ci-dessus'
            sh "docker stop test-${BUILD_NUMBER} || true"
            sh "docker rm test-${BUILD_NUMBER} || true"
        }

        always {
            echo "--- Fin du Build n°${BUILD_NUMBER} ---"
        }
    }
}