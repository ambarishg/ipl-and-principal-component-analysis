# Install the Azure Container Apps extension to the CLI.         
az extension add \
  --source https://workerappscliextension.blob.core.windows.net/azure-cli-extension/containerapp-0.2.0-py2.py3-none-any.whl      

# Register the Microsoft.Web namespace       
az provider register --namespace Microsoft.Web          

# Create the Resource group        
RESOURCE_GROUP="iplgroup2"
LOCATION="canadacentral"
LOG_ANALYTICS_WORKSPACE="ipl-logs"
CONTAINERAPPS_ENVIRONMENT="ipl-env" 

az group create \
--name $RESOURCE_GROUP \
--location "$LOCATION"        

# Create an environment                
  
az monitor log-analytics workspace create --resource-group $RESOURCE_GROUP --workspace-name $LOG_ANALYTICS_WORKSPACE        

LOG_ANALYTICS_WORKSPACE_CLIENT_ID=`az monitor log-analytics workspace show --query customerId -g $RESOURCE_GROUP -n $LOG_ANALYTICS_WORKSPACE --out tsv`             

LOG_ANALYTICS_WORKSPACE_CLIENT_SECRET=`az monitor log-analytics workspace get-shared-keys --query primarySharedKey -g $RESOURCE_GROUP -n $LOG_ANALYTICS_WORKSPACE --out tsv`           

az containerapp env create \
--name $CONTAINERAPPS_ENVIRONMENT \
--resource-group $RESOURCE_GROUP \
--logs-workspace-id $LOG_ANALYTICS_WORKSPACE_CLIENT_ID \
--logs-workspace-key $LOG_ANALYTICS_WORKSPACE_CLIENT_SECRET \
--location "$LOCATION"               

# Create a Azure Container Registry   ( Run in Console )   
az acr create --resource-group iplgroup2 --name agiplacr2 --sku Basic 

# Login into the Azure Container Registry ( Run in Console)     
az acr login -n agiplacr2   

# Tag image ( Run in Console)      

docker tag ipl:latest agiplacr2.azurecr.io/ipl:v1   

# Push image ( Run in Console)    
docker push agiplacr2.azurecr.io/ipl:v1

# Update the  Azure Container Registry ( Run in Console) 
az acr update -n agiplacr2 --admin-enabled true       

# Get the password of the Azure CLI ( Run in Azure CLI )   
password=$(az acr credential show --name agiplacr2 --query passwords[0].value --output tsv)

# Create the Container App           
az containerapp create \
--name iplapp4 \
--resource-group $RESOURCE_GROUP \
--environment $CONTAINERAPPS_ENVIRONMENT \
--image agiplacr2.azurecr.io/ipl:v1  \
--registry-login-server agiplacr2.azurecr.io \
--registry-username agiplacr2 \
--registry-password $password  \
--target-port 8501 \
--ingress 'external' \
--query configuration.ingress.fqdn

# References         
https://docs.microsoft.com/en-us/azure/container-apps/get-started?ocid=AID3042118&tabs=bash             