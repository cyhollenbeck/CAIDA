cls

# Variables
$subscriptionId = "6d1bfcff-db0e-40c9-851d-39f403e44c61"
$resourceGroupName = "rs-caida"
$location = "EastUS"
$serverName = "caida-postgres-server"
$databaseName = "caida-db"
$adminUser = "caidaadmin"
$adminPassword = "Sn@rPHM3AndYou!!"  # Replace with a strong password
$datasetPath = "datasets\azure.db"  # Path to your dataset file

# Log in to Azure using az CLI
az login

# Set the subscription context
az account set --subscription $subscriptionId

# Load environment variables from .env file
$envFilePath = ".\local.env"
if (Test-Path $envFilePath) {
    Get-Content $envFilePath | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+)=(.*)\s*$") {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
        }
    }
}

# Set environment variables for your Azure App Service
$envVars = @{
    "DB_USER"     = $env:DB_USER
    "DB_PASSWORD" = $env:DB_PASSWORD
    "DB_HOST"     = $env:DB_HOST
    "DB_PORT"     = $env:DB_PORT
    "DB_NAME"     = $env:DB_NAME
}

foreach ($key in $envVars.Keys) {
    az webapp config appsettings set --resource-group $resourceGroupName --name $serverName --settings "$key=$($envVars[$key])"
}