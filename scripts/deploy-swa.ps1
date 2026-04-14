param(
    [string]$EnvironmentName = "production"
)

$token = $env:AZURE_STATIC_WEB_APPS_API_TOKEN

if ([string]::IsNullOrWhiteSpace($token)) {
    Write-Error "Missing AZURE_STATIC_WEB_APPS_API_TOKEN environment variable."
    Write-Output "Set it for this session with:"
    Write-Output "  $env:AZURE_STATIC_WEB_APPS_API_TOKEN = '<your-token>'"
    exit 1
}

Write-Output "Deploying current folder to Azure Static Web Apps environment '$EnvironmentName'..."
npx @azure/static-web-apps-cli@latest deploy . --deployment-token "$token" --env "$EnvironmentName"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Deployment failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Output "Deployment completed successfully."
