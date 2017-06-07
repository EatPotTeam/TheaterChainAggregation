#!/usr/bin/env groovy

pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'No build needed!'
            }
        }

        stage('Test') {
            steps {
                echo 'No test available!'
            }
        }

        stage('Deploy') {
            steps {
                sh 'pm2 startOrRestart ecosystem.config.js --env dev'
            }
        }
    }
}