cls

# Load environment variables from .env file
$envFilePath = "C:\Users\chollenbeck\source\SourceVHD\cyhollenbeck\caida\local.env"
if (Test-Path $envFilePath) {
    Get-Content $envFilePath | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+?)\s*=\s*(.+?)\s*$") {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2])
        }
    }
}

# Variables
$subscriptionId = "6d1bfcff-db0e-40c9-851d-39f403e44c61"
$resourceGroupName = "rs-caida"
$location = "EastUS"
$serverName = "caida-postgres-server"
$databaseName = $env:DB_NAME
$adminUser = $env:DB_USER
$adminPassword = $env:DB_PASSWORD
$dbhostname = $env:DB_HOST
$dbport = $env:DB_PORT
$datasetPath = "C:\Users\chollenbeck\source\SourceVHD\cyhollenbeck\caida\datasets\azure.db"  # Path to your dataset file
$psqlpath = "C:\Program Files\PostgreSQL\16\bin\psql.exe"

# Log in to Azure using az CLI
##az login

# Set the subscription context
az account set --subscription $subscriptionId

# Set the password environment variable for psql
$env:PGPASSWORD = $adminPassword

# Convert SQLite database to SQL and pipe directly to PostgreSQL
$convertAndImportCommand = "sqlite3 $datasetPath .dump | `"$psqlpath`" --host=$dbhostname --port=$dbport --username=$adminUser --dbname=$databaseName --set=sslmode=require"

# Log the command being executed
Write-Output "Executing command: $convertAndImportCommand"

# Execute the command using cmd.exe /c and capture the output and errors
$output = & cmd.exe /c $convertAndImportCommand 2>&1

# Log the output and errors
Write-Output "Command output: $output"

# Check if the import was successful
if ($LASTEXITCODE -eq 0) {
    Write-Output "Import completed successfully."
} else {
    Write-Output "Import failed with exit code $LASTEXITCODE."
}