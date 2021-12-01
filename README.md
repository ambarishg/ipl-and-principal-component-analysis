This repository shows the following            
☑️ IPL Best Batsman using 6 different metrics and an unsupervised learning algorithm Principal Component Analysis for each of the seasons from 2007 to 2021             
☑️ IPL Best Bowler using 4 different metrics and an unsupervised learning algorithm Principal Component Analysis for each of the seasons from 2007 to 2021                
☑️ Create a Streamlit UI on top of the logic            
☑️ Create a Container Image and run it on local Docker            
☑️ Deploy the Container Image in Azure Container Instances         
☑️ Deploy the Container Image in Azure Kubernetes Cluster           
☑️ Deploy the Container Image in Azure Container Apps            

[Cricket Analytics Playlist](https://www.youtube.com/playlist?list=PL3mYo8cDslVW4ZGXujokM9S_iXMAXb0hE)              
This has videos on the calculation of the IPL best batsman and best bowler. This also has the details and inner workings of the PCA used in the analysis.           


|  FileName  |  Description |
|---|---|
|  Dockerfile | Docker file to produce a container image   |
|  requirements.txt | The libraries required for the Dockerfile are present in the requirements.txt. The Dockerfile uses the requirements.txt   |
|  Docker_steps.md | The steps required to deploy the container in the local Docker Desktop   |
|  azure_aci_steps.md | Steps to deploy in Azure Container Instance  |
|  service_principal_aks_steps.md | Steps to deploy in Azure Kubernetes Service  |
|  azure_container_apps.md | Steps to deploy in Azure Container Apps  |
|  ALL_2021_IPL_MATCHES_BALL_BY_BALL.csv | IPL Ball by Ball data - 2021  |
|  all_matches_details.csv | IPL Ball by Ball data for seasons 2007 to 2021  |
analysis-bowler-pca-details
|  analysis-bowler-pca-details.ipynb | This has the details of the IPython notebook for the PCA implementation  |

# PCA interesting research paper
[Anomaly Detection in Resource Constrained Environments With Streaming Data](https://www.amii.ca/latest-from-amii/anomaly-detection-resource-constrained-environments-streaming-data/)