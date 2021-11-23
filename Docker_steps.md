docker build -t ipl .        

docker run -p 8501:8501 ipl   

docker tag ipl:latest ambarishg/ipl:v1   
docker push ambarishg/ipl:v1