$name = split-path -leaf $PSScriptRoot
$targetDir = "x:\_pipeline\salt\installers_salt\Bottleship"
& "c:\Program Files\7-Zip\7z.exe" u -xr!'.git' -xr!'*.*~' "${targetDir}\${name}.zip" "${PSScriptRoot}"
