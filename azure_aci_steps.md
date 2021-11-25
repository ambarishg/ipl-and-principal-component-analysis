# get the current default subscription using show
az account show --output table

# Create a Resource Group    ( Run in Console )       
az group create --location centralindia --resource-group iplgroup 

# Create a Azure Container Registry   ( Run in Console )   
az acr create --resource-group iplgroup --name agiplacr --sku Basic 

# Login into the Azure Container Registry ( Run in Console)     
az acr login -n agiplacr   

# Tag image ( Run in Console)      
docker tag ipl:latest agiplacr.azurecr.io/ipl:v1   

# Push image ( Run in Console)    
docker push agiplacr.azurecr.io/ipl:v1

# Update the  Azure Container Registry ( Run in Console) 
az acr update -n agiplacr --admin-enabled true       

# Get the password of the Azure CLI ( Run in Console )   
password=$(az acr credential show --name agiplacr --query passwords[0].value --output tsv)

# Create the Azure Container ( Run in Console )        
az container create  --resource-group iplgroup  \
--name ipl --image agiplacr.azurecr.io/ipl:v1  \
--registry-login-server agiplacr.azurecr.io \
--ip-address Public  --location centralindia  \
--registry-username agiplacr \
--registry-password $password  \
--ports 8501 --dns-name-label iplanalyst   

# Navigate to http://iplanalyst.centralindia.azurecontainer.io:8501/

# Cleanup ( Run in Console)   
az group delete --resource-group iplgroup






