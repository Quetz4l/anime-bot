from PIL import Image
from service import parsing
from io import BytesIO


async def default_converting(source_image=None, url=None):
    image = await check_url_and_download_if_true(source_image, url)
    image = Image.open(BytesIO(image))
    image = image.resize((150, 225))
    return await save(image)

async def download_image(url):
    return parsing.get_html(url).content


async def check_url_and_download_if_true(source_image=None, url=None):
    if source_image is None and url is None:
        raise Exception('Не передана картинка')

    if source_image is not None:
        return source_image
    elif url is not None:
        return await download_image(url)


async def save(image):
    img_bio = BytesIO()
    image.save(img_bio, 'JPEG', quality=100)
    img_bio.seek(0)
    return img_bio
