

cls

# Clean the wwwroot directory on Azure
$cleanScript = @"
cd /home/site/wwwroot
rm -rf *
"@
Invoke-AzWebAppCommand -ResourceGroupName "rs-caida" -Name "caida" -Command $cleanScript