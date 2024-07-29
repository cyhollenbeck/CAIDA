# Variables
$subscriptionid = "6d1bfcff-db0e-40c9-851d-39f403e44c61"
$resourceGroupName = "rs-caida"
$location = "EastUS"
$serverName = "caida-postgres-server"
$databaseName = "caida-db"
$adminUser = "caidaadmin"
$adminPassword = "Sn@rPHM3AndYou!!"  # Replace with a strong password
$datasetPath = "datasets\azure.db"  # Path to your dataset file

# Login to Azure
##az login

# Set the subscription
az account set --subscription $subscriptionid

# Create a resource group
##az group create --name $resourceGroupName --location $location

# Create a PostgreSQL server
##az postgres server create --resource-group $resourceGroupName --name $serverName --location $location --admin-user $adminUser --admin-password $adminPassword --sku-name B_Gen5_1 --version 11

# Configure a firewall rule to allow access from all Azure services
##az postgres server firewall-rule create --resource-group $resourceGroupName --server $serverName --name AllowAllAzureIPs --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0

# Create a database
##az postgres db create --resource-group $resourceGroupName --server-name $serverName --name $databaseName

# Set environment variables
[System.Environment]::SetEnvironmentVariable('DB_USER', $adminUser, [System.EnvironmentVariableTarget]::Machine)
[System.Environment]::SetEnvironmentVariable('DB_PASSWORD', $adminPassword, [System.EnvironmentVariableTarget]::Machine)
[System.Environment]::SetEnvironmentVariable('DB_HOST', "$($serverName).postgres.database.azure.com", [System.EnvironmentVariableTarget]::Machine)
[System.Environment]::SetEnvironmentVariable('DB_PORT', '5432', [System.EnvironmentVariableTarget]::Machine)
[System.Environment]::SetEnvironmentVariable('DB_NAME', $databaseName, [System.EnvironmentVariableTarget]::Machine)


# Output the connection string
$connectionString = "postgresql://$($adminUser):$($adminPassword)@$($serverName).postgres.database.azure.com:5432/$($databaseName)"
Write-Output "Connection string: $connectionString"

# Import the dataset into the PostgreSQL database
$env:PGPASSWORD = $adminPassword
psql -h "$($serverName).postgres.database.azure.com" -U $adminUser -d $databaseName -f $datasetPath