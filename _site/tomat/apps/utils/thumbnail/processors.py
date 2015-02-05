# -*- coding: utf-8 -*_

import os.path
import PIL.Image

from django.conf import settings
from django.contrib.staticfiles import finders


_WATERMARK_PATH = finders.find('img/watermark.png')


def watermark_processor(image, **kwargs):
    try:
        image = image.convert('RGBA')
        watermark = PIL.Image.open(open(_WATERMARK_PATH))
        if image.size[0] < watermark.size[0] or image.size[1] < watermark.size[1]:
            return image

        top_left = (
            image.size[0] - watermark.size[0],
            image.size[1] - watermark.size[1]
        )

        resized = PIL.Image.new('RGBA', image.size)
        resized.paste(watermark, top_left)


        image.paste(watermark, top_left, watermark)

        return image

    except Exception as e:
        import traceback; traceback.print_exc()