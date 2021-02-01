import flip
import numpy as np
import uuid
import cv2
import os
import re
import matplotlib.pyplot as plt
from glob import glob

"""
Generate dataset with synthetic data
"""

# ============================================================================
# Functions
# ============================================================================


def generate_data(n_samples=5, n_objects=3, objects_pattern="objects/*",
                  backgrounds_pattern="backgrounds/*", show=False,
                  output_dir="data/noisy/noisy_img"):
    """
    Function that creates and setups the global variables and
    start the creation of the data

    - n_samples: number of new images to create for each background
    - n_objects: object number to place in each new image
    - objects_pattern: path where are the images to use as objects or noise
    - backgrounds_pattern: path where are the images to use as background
    - show: if True it shows some images created else they are not shown
    - output_dir: path where the generated images will be saved
    """

    # Environment global variables
    global N_SAMPLES
    global BACKGROUNDS_PATTERN
    global OBJECTS_PATTERN
    global OUTPUT_DIR
    global N_OBJECTS
    global SHOW

    # Setup global variables
    SHOW = show
    N_SAMPLES = n_samples
    BACKGROUNDS_PATTERN = backgrounds_pattern
    OBJECTS_PATTERN = objects_pattern
    OUTPUT_DIR = output_dir
    N_OBJECTS = n_objects

    # creates an empty folder
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    setup_environment(OBJECTS_PATTERN, BACKGROUNDS_PATTERN, N_SAMPLES)


def setup_environment(objects_pattern, backgrounds_pattern, n_samples):
    """
    Call function that generates synthetic data
    and shows some images if SHOW is True

    - objects_pattern: path for objects images
    - backgrounds_pattern: path for background images
    - n_samples: number of new images to create for each background
  """

    # get object paths
    objects_paths = glob(objects_pattern)

    # get background paths
    backgrounds_paths = glob(backgrounds_pattern)

    if SHOW is True:
        n_background = len(backgrounds_pattern)
        n_w = 6
        n_h = 5
        fig = plt.figure(figsize=(n_h, n_w))
        n_fig = 1
        aux = 1

    # iterate all backgrounds
    for idx in range(len(backgrounds_paths)):

        if SHOW is True and aux <= n_h:
            background = flip.utils.inv_channels(
                cv2.imread(backgrounds_paths[idx], cv2.IMREAD_UNCHANGED)
            )
            fig.add_subplot(n_h, n_w, n_fig)
            plt.title("original")
            plt.imshow(background)
            plt.axis("off")
            n_fig += 1
            aux += 1
            temp = 1

        # create a new image until reaching n_samples
        for sample in range(n_samples):
            try:
                el = create_element(objects_paths, backgrounds_paths[idx])
            except:
                print(backgrounds_paths[idx])

            if SHOW is True and temp <= n_w - 1:
                image = el.created_image
                fig.add_subplot(n_h, n_w, n_fig)
                plt.title(sample + 1)
                plt.imshow(image)
                plt.axis('off')
                n_fig += 1
                temp += 1

        if SHOW is True and aux == n_h + 1:
            plt.tight_layout(pad=2)
            plt.show()
            aux += 1


def create_element(objects_paths, background_path):
    """
    Function that generates and saves the synthetic images

    - objects_paths: path where images that will be used as elements are saved
    - background_path: path where images that will be used as backgrounds are

    Returns: Element class instance
    """
    # Check if N_OBJECTS is iterable and define amount of objects
    if hasattr(N_OBJECTS, "__iter__"):
        n_objs = np.random.randint(low=N_OBJECTS[0], high=N_OBJECTS[1] + 1)
    else:
        n_objs = N_OBJECTS

    # get random elements
    object_idxs = np.random.choice(objects_paths, n_objs)
    # print(object_idxs)

    # Create elements for the object images
    objects = [create_child(i) for i in object_idxs]

    # get background
    background_image = flip.utils.inv_channels(
        cv2.imread(background_path, cv2.IMREAD_UNCHANGED,)
    )

    # create new element
    el = flip.transformers.Element(image=background_image, objects=objects)

    # Transformer element
    transform_objects = [
        flip.transformers.data_augmentation.Rotate(mode='random', min=0, max=5),
        flip.transformers.data_augmentation.Flip(mode='y'),
        flip.transformers.data_augmentation.RandomResize(
            mode='symmetric_w',
            relation='parent',
            w_percentage_min=0.05,
            w_percentage_max=0.3,
        ),
    ]

    name1 = background_path.split("\\")[1].split(".")[0]
    name = name1 + "__" + str(uuid.uuid4())

    transform = flip.transformers.Compose(
        [
            flip.transformers.ApplyToObjects(transform_objects),
            flip.transformers.domain_randomization.ObjectsRandomPosition(
                x_min=0.07,
                y_min=0.01,
                x_max=0.9,
                y_max=0.6,
                mode='percentage',
                overlap=0.05
            ),
            flip.transformers.domain_randomization.Draw(),
            flip.transformers.labeler.CreateBoundingBoxes(),
            flip.transformers.io.SaveImage(OUTPUT_DIR, name)
        ]
    )

    [el] = transform(el)

    # Generate label files
    labeling(el, name)
   
    return el

def labeling(el, name):
    """
    Function that generates label files and save them in the OUTPUT_DIR

    - el: Element class instance
    - name: image name
    """

     # get image dimensions
    w_img = el.image.shape[1]
    h_img = el.image.shape[0]

    # get all objects located in the image
    tags = el.tags

    txt_path = f"{OUTPUT_DIR}/{name}.txt"

    for tag in tags:
        
        # save the x values of the upper left coordinate
        x = tag['pos']['x']

        # save the y values of the upper left coordinate
        y = tag['pos']['y']

        # save object width
        w = tag['pos']['w']

        # save object height
        h = tag['pos']['h']

        # adjust values if object sticks out of image
        if h + y > h_img:
            h = h_img - y

        if w + x > w_img:
            w = w_img - x

        # calculate x center and y center, and calculate proportion
        xcen = (x + w /2) / w_img
        ycen = (y + h /2) / h_img

        w /= w_img
        h /= h_img

        # writing format: class x_center y_center width height and line break
        txt_data = f"0 {xcen:6f} {ycen:6f} {w:6f} {h:6f}\n"

        # write information to a txt file with the same name as the image
        with open(txt_path, mode="a") as f:
            f.write(txt_data)


def create_child(path):
    """
    Function that creates child-type instances of the Element class

    Return: Element instance
    """

    # reads image and changes the order of channels
    img = flip.utils.inv_channels(cv2.imread(path, cv2.IMREAD_UNCHANGED))

    # saves image name
    split_name_temp = re.split(r"/|\\", path)
    index = len(split_name_temp) - 1
    split_name = split_name_temp[index] if index >= 0 else split_name_temp[0]

    # creates Element child instance
    element_instance = flip.transformers.Element(image=img, name=split_name)

    return element_instance

# ==============================================================================

if __name__ == "__main__":
    generate_data(n_samples=1,
                n_objects=3,
                backgrounds_pattern="backgrounds/*",
                objects_pattern="objects/*",
                output_dir="obj",
                show=False)
