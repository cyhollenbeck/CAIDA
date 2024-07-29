
$sqlFilePath = "C:\Users\chollenbeck\source\SourceVHD\cyhollenbeck\caida\datasets\azure.db" 

Get-Content $sqlFilePath | Set-Content -Encoding UTF8 $sqlFilePath