import skimage.io
from skimage.transform import resize


def make_thumb(path, thumb_path, size=(160, 120)):
    image = skimage.io.imread(path)
    height, width = image.shape[0], image.shape[1]

    thumb = image

    if (height / width) > (size[0] / size[1]):
        new_height = width * size[0] // size[1]
        height1 = (height - new_height) // 2
        thumb = image[height1:height + new_height, 0:width]

    if (height / width) < (size[0] / size[1]):
        new_width = height * size[1] // size[0]
        width1 = (width - new_width) // 2
        thumb = image[0:int(height), int(width1):int(width1 + new_width)]

    thumb = resize(thumb, size)
    print(thumb.shape)
    skimage.io.imsave(thumb_path, thumb)
    return thumb
