# Image Rest API


## Upload an Image:
	 Call type: POST
	 URL: http://127.0.0.1:5000/images
	 Key: image
	 Responses:
		OK - If image isn't already in database:
			State: 200 OK
			{
			    "new": true,
				"url": "/images/bbef1c9860914f46"
			}

		OK - If image is already in the database:
		    State: 200 OK
			{
				"new": false,
				"url": "/images/bbef1c9860914f46"
			}

		ERROR - If no image is sent in the request:
			State: 400 BAD REQUEST
			"Please upload a valid file."

		ERROR - If the file is bigger than 25 megabytes:
			State: 400 BAD REQUEST
			"The file is too big. Maximum size = 25 megabytes."

		ERROR - If the file is not an image:
			State: 400 BAD REQUEST
			"Invalid file format, please upload an image (for example jpeg or png)."

		

## Download an Image:
	Call type: GET
	URL http://127.0.0.1:5000/images/<id_image>
	Responses:
		OK - id is found in the database:
			State: 200 OK
			File: Original file in jpg format.

		ERROR - id is not found in database
			State: 400 BAD REQUEST
			"No image with the provided id has been found, please provide a valid id."
			
			
## Docker Build:
### Image:
        Go to project directory.
        Run "docker build -t images:latest ." (whithout the quotes).
    
### Container:
        Run "docker run -it -d -p 5000:5000 images" (whithout the quotes).
        See running containers: docker ps
        Stop container: docker stop ContainerID
        Start container: docker start ContainerID
        
        To use the images app please refer to the top of the document.
  