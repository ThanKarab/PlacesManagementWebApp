# Places Management WebApp
A simple webapp for managing places. Developed with Python, Django DRF, SQLite.


### Installation

1. Install `docker`.

1. Build the image:
    ```
    docker build -t places .
    ```

1. Start the container:
   ```
   docker run -d -p 8000:8000 --name app places
   ```

1. Create a superuser to be able to access the admin panel:
   ```
   docker exec -it app python manage.py createsuperuser
   ```

1. (Optional) Start the container with volume to persist data:
    ```
   docker run -d -p 8000:8000 -v /home/db:/opt/db --name app places
   ```

1. (Optional) Run the tests:
   ```
   docker exec -it app poetry run python manage.py test
   ```

1. Happy reviewing at http://127.0.0.1:8000/admin !
