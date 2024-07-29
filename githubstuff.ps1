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

# Navigate to the local Git directory
cd $localGitDirectory
echo "Navigated to local Git directory: $localGitDirectory"

# Initialize a Git repository if you haven't already
git init
echo "Initialized Git repository"

# Add Azure remote
$gitRemoteUrl = (az webapp deployment source config-local-git --name $webAppName --resource-group $resourceGroupName --query url --output tsv)
echo "Azure remote URL: $gitRemoteUrl"

# Check if remote already exists and remove it if it does
if (git remote | Select-String -Pattern "azure") {
    git remote remove azure
    echo "Removed existing Azure remote"
}

git remote add azure $gitRemoteUrl
echo "Added Azure remote"

# Add all changes to the staging area
git add .
echo "Staged all changes"

# Commit your code
git commit -m "Deploying to Azure"
echo "Committed changes"

# Increase Git buffer size
git config http.postBuffer 524288000
echo "Increased Git buffer size"

# Push the code to Azure
git push azure master --force
echo "Pushed code to Azure"