# Synthetic images
In this project, synthetic images are created with the flip library.
![image](https://github.com/xica369/synthetic_images_with_flip/blob/main/synthetic_images/image.jpg)

## Requirements
- [Python 3.7](https://www.python.org/downloads/ "Python 3.7")
- [Flip](https://pypi.org/project/flip-data/ "Flip")
- [Matplotlib](https://pypi.org/project/matplotlib/ "Matplotlib")

## How to use
- Clone the repository
- In the */backgrounds* folder save the images that you are going to use as backgrounds.
- In the */objects* folder save the images in png format and with a transparent background that will be used during the composition of the synthetic images.
- Open the file `create_synthetic_images.py` and in the last lines you can change the parameters of the function to generate the synthetic data.

```python
generate_data(n_samples=1,
              n_objects=4,
              backgrounds_pattern="backgrounds/*",
              objects_pattern="objects/*",
              output_dir="synthetic_images",
              show=False)
```
- 
  - **n_samples:** number of new images to create for each background
  - **n_objects:** number object to place in each new image. It can be an integer or a tuple. For example 3 -> will always put 3 objects, (2, 5) -> will put between 2 and 5 objects in each image
  - **backgrounds_pattern:** path where are the images to use as background
  - **objects_pattern:** path where are the images to use as objects
  - **output_dir:** path where the generated images will be saved
  - **show:** if True it shows some images created else they are not shown

- Save changes
- From the repository root run this command
```python
$ python ./create_synthetic_images.py
```
- The images created will be saved in the fodel */synthetic_images*
- If in addition to the synthetic images you also want to have the labeling files to train a YOLO model, you can execute the `create_synthetic_images_and_labeling.py` file which is like the `create_synthetic_images.py` file with an extra function that allows you to create the txt files.  From the repository root run this command
```python
$ python ./create_synthetic_images_and_labeling.py
```
For each synthetic image, a labeling file is created where each row is the information of each object in the image with the following format:
`class x_center y_center width height
`
for example:
`0 0.697266 0.503472 0.099609 0.222222`

## Author
[**Carolina Andrade**](https://www.linkedin.com/in/xicav369/)
