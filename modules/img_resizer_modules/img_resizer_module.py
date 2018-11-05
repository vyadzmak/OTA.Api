import models.app_models.setting_models.setting_model as settings

from PIL import Image

from resizeimage import resizeimage

def resize_image(file_path,output_path,target_size):
    try:
        with open(file_path, 'r+b') as f:
            with Image.open(f) as image:
                fill_color = '#FFFFFF'
                if image.mode in ('RGBA', 'LA'):
                    background = Image.new(image.mode[:-1], image.size, fill_color)
                    background.paste(image, image.split()[-1])
                    image = background

                if (image.mode in ('P')):
                    r_path =file_path.replace('/','\\')
                    t_image = Image.open(r_path).convert('RGB')
                    background =t_image
                    image = background
                resize_k =1
                original_width = image.width
                original_height = image.height

                target_width = target_size[0]
                target_height = target_size[1]

                if (original_width<=target_width and original_height<=target_height):
                    image.save(output_path,'JPEG')
                elif (original_width>original_height):
                    resize_k = target_width/original_width

                elif (original_height>=original_width):
                    resize_k = target_height/original_height

                out_width =round(original_width*resize_k,0)
                out_height = round(original_height*resize_k,0)

                cover = resizeimage.resize_cover(image, [out_width, out_height])
                cover.save(output_path, 'JPEG')

    except Exception as e:
        pass
