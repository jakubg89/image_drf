# Image API

### Overview
Simple DRF Api that allows users to upload images and receive URL to uploaded image based on tier permissions.

Each tier allows user to store up to 3 (original, small and medium) uploaded image in pre-defined size.

There are 3 build in tiers:
- **Basic** allows to store and get url to small image in maximum height of 200px
- **Premium** allows to store and get url to small image in maximum height of 200px, medium image in maximum height of 400px and orginal uploaded image
- **Enterprise** allows to store and get url to small image in maximum height of 200px, medium image in maximum height of 400px,  orginal uploaded image and ability to generate temporary urls.
- 
Custom tier can be created threw admin panel where:
- small image maximum height can be set
- medium image maxium height can be set
- give permission what images will be stored
- give permission what url can be generated

### Instalation

To run application you have to download repository from <a href="https://github.com/jakubg89/image_drf/archive/refs/heads/master.zip"> here</a>.

Extract data.

Run ```docker-compose up``` or ```docker-compose up -d``` to perform task in background.

After building container is finished we need to create superuser by command
```docker-compose run app python manage.py createsuperuser ```

Now we have access to API threw browser by opening ```127.0.0.1:8000```


### Endpoints
```/upload/``` - uploading image

```/image-list/``` - list of uploaded image by logged-in user

### Optimization

Checking views

![Alt text](before.jpg?raw=true "Title")

Optimizing view that generates most queries by adding related objects.

![Alt text](after.jpg?raw=true "Title")

