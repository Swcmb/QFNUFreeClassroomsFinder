import ddddocr
from io import BytesIO
from PIL import Image

ocr = ddddocr.DdddOcr()


def get_ocr_res(cap_pic_bytes):  # 识别验证码
    # 如果输入是PIL图像对象，则转换为字节
    if hasattr(cap_pic_bytes, 'save'):
        # 这是一个PIL图像对象，需要转换为bytes
        buffered = BytesIO()
        # 检查图像模式，确保兼容性
        if cap_pic_bytes.mode in ("RGBA", "P"):
            # 转换为RGB模式以避免某些格式问题
            if cap_pic_bytes.mode == "P":
                cap_pic_bytes = cap_pic_bytes.convert("RGBA")
            # 将RGBA转换为RGB，因为验证码通常是RGB格式
            if cap_pic_bytes.mode == "RGBA":
                background = Image.new("RGB", cap_pic_bytes.size, (255, 255, 255))
                background.paste(cap_pic_bytes, mask=cap_pic_bytes.split()[-1])
                cap_pic_bytes = background
        cap_pic_bytes.save(buffered, format=cap_pic_bytes.format or 'PNG')
        cap_pic_bytes = buffered.getvalue()
    
    res = ocr.classification(cap_pic_bytes)
    return res