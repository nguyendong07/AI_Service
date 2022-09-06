from paddleocr import PaddleOCR
#from PIL import Image
#import gradio as gr
#import torch
def inference(image_path):
    ocr = PaddleOCR(use_angle_cls=False, lang="en",use_gpu=False)
    img_path = "imgcrop.jpg"
    result = ocr.ocr(image_path, cls=True)
    #image = Image.open(img_path).convert('RGB')
    #boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    #scores = [line[1][1] for line in result]
    #im_show = draw_ocr(image, boxes, txts, scores,font_path='simfang.ttf')
    #im_show = Image.fromarray(im_show)
    #im_show.save('result.jpg')
    new_list = [replace(s) for s in txts]
    return '-'.join(new_list)
def replace(text):
    replacements = {
        "\\": "",
        "`": "",
        "*": "",
        "_": "",
        "{": "",
        "}": "",
        "[": "",
        "]": "",
        "(": "",
        ")": "",
        ">": "",
        "#": "",
        "+": "",
        ".": "",
        "!": "",
        "$": "",
    }
    text = "".join([replacements.get(c, c) for c in text])
    return text
