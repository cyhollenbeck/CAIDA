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

# Create the resource group
az group create --name $resourceGroupName --location $location

# Create the App Service plan
az appservice plan create --name $appServicePlanName --resource-group $resourceGroupName --location $location --sku B1 --is-linux

# Create the Web App
az webapp create --resource-group $resourceGroupName --plan $appServicePlanName --name $webAppName --runtime "PYTHON|3.12"

# Configure the Web App to use the Dockerfile
az webapp config container set --resource-group $resourceGroupName --name $webAppName --docker-custom-image-name "python:3.12"

# Set the Dockerfile path
az webapp config appsettings set --resource-group $resourceGroupName --name $webAppName --settings DOCKER_CUSTOM_IMAGE_NAME="python:3.12" DOCKERFILE_PATH="/Dockerfile"

# Configure deployment from GitHub
az webapp deployment source config --name $webAppName --resource-group $resourceGroupName --repo-url $gitRemoteUrl --branch "main" --manual-integration

# Verify the app settings
az webapp config appsettings list --resource-group $resourceGroupName --name $webAppName


# Variables
$subscriptionid = "6d1bfcff-db0e-40c9-851d-39f403e44c61"
$resourceGroupName = "rs-caida"
$webAppName = "caida"

# Login to Azure
az login

# Set the subscription
az account set --subscription $subscriptionid

# Add environment variables
az webapp config appsettings set --resource-group $resourceGroupName --name $webAppName --settings ENV_VAR1="value1"
az webapp config appsettings set --resource-group $resourceGroupName --name $webAppName --settings ENV_VAR2="value2"
az webapp config appsettings set --resource-group $resourceGroupName --name $webAppName --settings ENV_VAR3="value3"
az webapp config appsettings set --resource-group $resourceGroupName --name $webAppName --settings ENV_VAR4="value4"