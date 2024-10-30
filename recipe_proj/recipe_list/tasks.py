#from celery import shared_task
from django.conf import settings
from recipe_list.models import RecipeModel
from django.contrib.auth import get_user_model
from celery_app import app
import boto3
import random


@app.task()
def newRecipe(recipe_title,
              recipe_text,
              recipe_image,
              recipe_complexity,
              recipe_category,
              user,
              bytes_image) -> None:
   
    if 1 <= recipe_complexity <= 10 and (recipe_category, recipe_category) in settings.CATEGORY_LIST and recipe_image != '':
        url_img = uploadToS3(bytes_image, recipe_image)
        new_recipe = RecipeModel.objects.create(
            title=recipe_title,
            text_recipe=recipe_text,
            image_url=url_img,
            complexity=recipe_complexity,
            category=recipe_category,
            owner=get_user_model().objects.get(id=user)
        )


@app.task()
def updateRecipe(recipe_title,
                 recipe_text,
                 recipe_image,
                 recipe_complexity,
                 recipe_category,
                 recipe_id,
                 bytes_image):
    
    if 1 <= recipe_complexity <= 10 and (recipe_category, recipe_category) in settings.CATEGORY_LIST and recipe_image != '':
        url_img = uploadToS3(bytes_image, recipe_image)
        to_update = RecipeModel.objects.get(id=recipe_id)
        to_update.title = recipe_title
        to_update.text_recipe = recipe_text
        to_update.image_url = url_img
        to_update.complexity = recipe_complexity
        to_update.category = recipe_category
        to_update.save(
            update_fields=["title", 'text_recipe', 'image_url', 'complexity', 'category'])


def uploadToS3(image: bytes, name: str) -> str:
    conf = {
        'aws_access_key_id': settings.S3_ACCESS_KEY,
        'aws_secret_access_key': settings.S3_SECRET_KEY,
        'endpoint_url': settings.S3_ENDPOINT_URL,
        'region_name': settings.S3_REGION_NAME
    }
    client = boto3.client('s3', verify=False, **conf)
    list_names = []
    for i in client.list_objects(Bucket=settings.S3_BUCKET_NAME)["Contents"]:
        list_names.append(i['Key'])
    for i in range(100):
        file_name = str(random.randint(1, 1000)) + "_" + name
        if file_name not in list_names:
            break
    else:
        return ""
    client.put_object(
        Bucket=settings.S3_BUCKET_NAME,
        Key=file_name,
        Body=image
    )
    client.close()
    return f"https://15545f35-0713-421c-818e-133cecbc2a8e.selstorage.ru/" + file_name
