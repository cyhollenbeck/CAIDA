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
##az login

# Set the subscription
az account set --subscription $subscriptionid

# Create a Resource Group if it doesn't exist
##az group create --name $resourceGroupName --location $location


# Create a Linux App Service Plan 
##az appservice plan create --name $appServicePlanName --resource-group $resourceGroupName --location $location --sku B1 --is-linux


# Create the web app with the Python 3.12 
##az webapp create --resource-group $resourceGroupName --plan $appServicePlanName --name $webAppName --runtime "PYTHON:3.12"


# Navigate to the local Git directory
cd $localGitDirectory
echo here1

# Initialize a Git repository if you haven't already
git init
echo here2
# Add Azure remote
$gitRemoteUrl = (az webapp deployment source config-local-git --name $webAppName --resource-group $resourceGroupName --query url --output tsv)

git remote add azure $gitRemoteUrl

echo here3

# Commit your code
git add .
git commit -m "Initial commit"

echo here4

# Push your code to Azure
git push azure master

echo here5
# Set the startup command (optional, adjust as needed)
az webapp config set --resource-group $resourceGroupName --name $webAppName --startup-file "startup.sh"

echo here6



