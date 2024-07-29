
# Clear the screen
cls

# Variables
$subscriptionid = "6d1bfcff-db0e-40c9-851d-39f403e44c61"
$resourceGroupName = "rs-caida"
$location = "EastUS"
$appServicePlanName = "ap-service-caida"
$webAppName = "caida"
$localGitDirectory = "C:\~Drives\DataVHD\myAIone"
$gitRemoteUrl = "https://github.com/cyhollenbeck/CAIDA"


# Login to Azure
az login

# Set the subscription
az account set --subscription $subscriptionid

###az webapp config appsettings set --resource-group $resourceGroupName --name $webAppName --settings DATABASE_URL="your_database_connection_string"


##az webapp deployment source config --name $webAppName --resource-group $resourceGroupName --branch master


#!/bin/bash
##export FLASK_APP=app.py
##flask run --host=0.0.0.0 --port=8000


cd $localGitDirectory

# Check current branch
##git branch

# If not on master, switch to master
##git checkout master

# Ensure master is the default branch
##git branch -M master

##git add .
##git commit -m "Deploying Flask app with SQLite to Azure"
##git push azure master


##az webapp config set --resource-group $resourceGroupName --name $webAppName --startup-file "startup.sh"

##https://portal.azure.com/#@nebiolabs.onmicrosoft.com/resource/subscriptions/6d1bfcff-db0e-40c9-851d-39f403e44c61/resourceGroups/rs-caida/providers/Microsoft.Web/sites/caida/config/logs



##az webapp log config --name $webAppName --resource-group $resourceGroupName --application-logging filesystem --detailed-error-messages true


##az webapp log show --name $webAppName --resource-group $resourceGroupName

##az webapp log config --name $webAppName --resource-group $resourceGroupName --web-server-logging filesystem

##az webapp log tail --name $webAppName --resource-group $resourceGroupName

az webapp config container set --resource-group "rs-caida" --name "caida" --docker-custom-image-name "python:3.12"



az webapp config appsettings set --resource-group "rs-caida" --name "caida" --settings DOCKER_CUSTOM_IMAGE_NAME="python:3.12" DOCKERFILE_PATH="/Dockerfile"