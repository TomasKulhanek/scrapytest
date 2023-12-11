sudo docker stop sreality
sudo docker remove sreality
sudo docker run --name sreality -e POSTGRES_PASSWORD=vagrant -p 5432:5432 -d postgres
