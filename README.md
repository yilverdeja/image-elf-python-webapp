<img src="static/logos/logo-gradient.svg" width="72"/>

# img-elf 	📸🧝🧝🏻🧝🏼🧝🏽🧝🏾🧝🏿

A simple flask app to create custom sized dummy images for testing

![image](https://github.com/user-attachments/assets/67f2dc92-67ab-4cc4-863d-5a76b761f57b)

## Features

Create an image given a specified width, height, and an image output format:

- Width: A positive integer between 1 and 10000px
- Height: A positive integer between 1 and 10000px
- Type: An image of type `PNG` or `JPEG`

## Getting Started

### Docker

To quickly start the application without building the Docker image locally, you can use the following command:

```bash
# runs the yilverdeja/image-elf image on host port 5100 from container port 5100
docker run -p 5100:5100 yilverdeja/image-elf
```

To run and setup the docker file locally, you can use the following commands:

```bash
# build image
docker build -t image-elf .

# run image on host port 5100 from container port 5100
docker run -p 5100:5100 image-elf
```

### Development

```bash
pip install -r requirements.txt
python app.py
```

## Why?

The purpose of this project was to learn to use Docker to deploy a simple cloud application. This image was pushed to the `google artifact registry`, and then created a `service` on `google cloud run`.

### Requirements

To deploy this application on the cloud, you need to have configured:

- [Docker](https://www.docker.com/)
- [gcloud client](https://cloud.google.com/sdk/docs/install)

### Setup

1. Create new `google cloud` project or use existing one
2. Enable `Artifact Registry`
3. Create a new repository. Before clicking `Create`, Name the project (i.e. `image-elf`) and choose `region`, and leave everything else as is.
4. On the repositories page, select the repository created (i.e. `image-elf`)
5. Copy the repostiory path (i.e. `<region>-docker.pkg.dev/<project-id>/image-elf`)
6. Build the image and tag it with the repository path copied above and add a tag name (i.e. `<region>-docker.pkg.dev/<project-id>/image-elf/<image-name>`)

   assuming `region` is **asia-east1** and `project-id` is **project-12345**

   ```bash
   # build the tag
   docker build -t asia-east1-docker.pkg.dev/project-12345/image-elf/image-elf

   # push the image
   docker push asia-east1-docker.pkg.dev/project-12345/image-elf/image-elf
   ```

7. Back on `google cloud` platform, go to `Cloud Run` and click `Deploy Container` and select `Service`
8. Configure the service:
   - Check 'Deploy one revision from an existing container image'
   - Select recently pushed container image from the `Artifact Registry`
   - Add a `Service Name` (i.e. image-elf)
   - For basic usage & testing, set to `Authentication` to "Allow unathenticated invocations"
   - Set `CPU Allocation` to "CPU is only allocated during request processing". Keep `minimum number of instances` at 0 to reduce costs in keeping it always available
   - On Container editing, set container port to `5100` and choose how many resources to allocate for the container (i.e. 1GiB and 1CPU). Choose the min and max instances for `revision autoscaling` (i.e. 0 and 3)
9. Click `Create` service and wait for it to be deployed

## Improvements

To improve this functionality of this tool:

- Catch `MemoryError` exceptions and handle accordingly
- Add more configurations:
  - Select Background color (single color, or noise)
  - Choose to Show/Hide text
  - More image types
- Image file size estimator on client before creating image
- Create images in bulk using `yaml` / `yml` or `json` by allowing users to specify requirements in a file
