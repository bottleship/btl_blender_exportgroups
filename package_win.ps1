$ignore = @(".git")
Get-ChildItem $PSScriptRoot | where { $_.Name -notin $ignore } | Compress-Archive -DestinationPath "${PSScriptRoot}.zip" -Update
