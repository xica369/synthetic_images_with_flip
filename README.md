# Synthetic images
In this project, synthetic images are created with the flip library.

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
              backgronds_pattern="backgrounds/*",
              objects_pattern="objects/*",
              output_dir="synthetic_images",
              show=False)
```
**n_samples:** number of new images to create for each background
**n_objects:** object number to place in each new image
**backgrounds_pattern:** path where are the images to use as background
**objects_pattern:** path where are the images to use as objects
**output_dir:** path where the generated images will be saved
**show:** if True it shows some images created else they are not shown

## Author
[**Carolina Andrade**](https://www.linkedin.com/in/xicav369/)
