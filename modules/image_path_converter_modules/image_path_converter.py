import urllib.parse
import models.app_models.setting_models.setting_model as settings

def convert_path(entity):
    try:
        api_url = settings.API_URL
        if (entity.file_path != None):
            entity.file_path = urllib.parse.urljoin(api_url, entity.file_path)

        if (entity.thumb_file_path != None):
            entity.thumb_file_path = urllib.parse.urljoin(api_url, entity.thumb_file_path)

        if (entity.optimized_size_file_path != None):
            entity.optimized_size_file_path = urllib.parse.urljoin(api_url, entity.optimized_size_file_path)
        pass
    except Exception as e:
        pass