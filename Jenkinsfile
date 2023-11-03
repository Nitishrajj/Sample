pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                bat 'build.bat' // Use 'bat' for Windows batch scripts
            }
        }
        stage('Run Application') {
            steps {
                bat 'run_app.bat' // Use 'bat' for Windows batch scripts
            }
        }
    }
}
