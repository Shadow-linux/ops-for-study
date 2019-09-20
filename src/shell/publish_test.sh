#!/usr/bin/env bash


ProjectName=${1}
Environment=${2}
Action=${3}
TaskID=${4}
IsJacoco=${5}
Version=${6}
PublishIP=${7}
ServerMode=${8}
Branch=${9}

echo "ProjectName=${1}"
echo "Environment=${2}"
echo "Action=${3}"
echo "TaskID=${4}"
echo "IsJacoco=${5}"
echo "Version=${6}"
echo "PublishIP=${7}"
echo "ServerMode=${8}"
echo "Branch=${9}"

source ./ops_control.sh


function UtilSleep() {
    for _ in $(seq 1 5);do
        echo ". " && sleep 1
    done
}

function AppConfig() {
    echo "Get App Config ..."
    UtilSleep
}


function CodeBuild() {
    echo "Code Build ..."
    UtilSleep
    CommitPublishStatus ${TaskID} 'code_build'
}


function GitClone() {
    echo "Git Clone ..."
    UtilSleep
    CommitPublishStatus ${TaskID} 'git_clone'
}


function DockerBuild() {
    echo "Docker Build ..."
    UtilSleep
    CommitPublishStatus ${TaskID} 'docker_build'
}


function UploadRepo() {
    echo "Upload Repo ..."
    UtilSleep
    CommitPublishStatus ${TaskID} 'upload_repo'
}


function DownloadRepo() {
    echo "Download Repo ..."
    UtilSleep
    CommitPublishStatus ${TaskID} 'download_repo'
}


function DeployApp() {
    echo "Deploy App ..."
    UtilSleep
    CommitPublishStatus ${TaskID} 'deploy_app'
}


function RestartApp() {
    echo "Restart App ..."
    UtilSleep
    CommitPublishStatus ${TaskID} 'restart_app'
}


function Done() {
    echo "Done."
    CommitPublishStatus ${TaskID} 'done'
}


function ActionRouter () {
    local action=${1}
    case ${action} in
    'Deploy')
        GitClone
        CodeBuild
        DockerBuild
        UploadRepo
        DeployApp
        RestartApp
        Done
        ;;
    'DeploySync')
        DownloadRepo
        DeployApp
        RestartApp
        Done
        ;;
    'Rollback')
        DownloadRepo
        DeployApp
        RestartApp
        Done
        ;;
    *)
        echo 'No action to do.'
        exit 1
    esac
}



function Main () {
    local action=${1}
    echo "Test Code Publish ..."
    ActionRouter ${action}
}

Main ${Action}