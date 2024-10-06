# Visage-ML

Visage-ML is a series of tools to do facial recognition on images (and create a
searchable database).

# Create you own database

## Get a folder with images

using the following folder structure.

```
person_name
  - image_file_001.jpeg
  - another_01.jpeg
```

where `person_name` could be a person_name name or a UID, anything unique.

## run the hasher

First we need to download some weights so the model can run.

download the following to files and put them in `/hasher/weights`

```
https://github.com/serengil/deepface_models/releases/download/v1.0/facenet512_weights.h5
https://github.com/serengil/deepface_models/releases/download/v1.0/retinaface.h5
```

In the hasher folder, modify the docker-compose to point to your folder of
images.

```
docker-compose build
docker-compose up
```

Once complete, It creates a sidecar file called <image name>.vector next to it
each image.

## run the builder

To create the database that can be used to lookup, we use the `builder`

same thing as before, modify the docker-compose file.

```
docker-compose build
docker-compose up
```

This should give two files at the root of the folder you made available the
container.

`face.db` and `face.json` these files are used by the next container.

## run the face matcher

Once again. modify the docker-compose.

You'll need to create the file `matcher/performers.json` for the container to
build. It should have contents like this:

```
{
"93aa1a98-e86e-47a2-b661-f5d703a6e727":"0005"
}
```

where the key is a performer's stash_id and the value is a performer's name.

You'll also need to copy `face.db` and `face.json` from the previous step to
the `matcher/` directory.

After that, run `docker-compose up`. It will run `main.py` will run and create
`<image name>.json` file(s) for each vector in the directory, each containing
the 10 closest results.

If you're interested to compile the results of a directory of matches, you can
do so like this:

`python scoring.py --performers-file performers.json /tmp/images/`

You'll get some output to stdout like this:

```
Score   Hits    Avg Distance    ID      Name
0.75    9       11.93   fe6d11a2-fb64-498d-bdb7-c1d97d079c8b    Miss Lexa
0.61    7       11.55   fe2faf98-6a14-4b93-88f1-9989779eeaeb    Sage
0.57    4       7.07    a33862fc-5be7-412f-9d1b-bde39f2e1700    Diana Daniels
0.53    7       13.19   fa57d66c-d523-4a56-80ff-83fd8bb076c6    MysteriousKathy
0.42    5       11.92   46b28f9b-e150-4af0-a26d-6d29d7b116d5    Mia Love
```

## Known issues and missing features

- [ ] No error messages are show in the UI
  - [ ] When no face can be detected
  - [ ] When no result is returned from the API
  - [ ] When creating a performer from stashbox but the local stash instance is giving a checksum error
- [ ] Scan a region of the screen to scan a single performer
- [ ] Scan for multiple performers
- [ ] On matches, link to stashbox so person can check other photo's of performer
