import requests
import os
import openai
from PIL import Image

#open ai api key
openai.api_key = os.getenv("OPENAI_API_KEY")

#provide the folder path where you want to save the image
destination_path = 'gen_images'

# some prompt
prompt="a close up, studio photographic portrait of a white siamese cat that looks curious, backlit ears"

def dalle_create_img(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
        )
    image_url = response['data'][0]['url']
    return {'created':response['created'], 
            'url':image_url}

def download_image(image, destination_path):
    # Fetch the image from the URL
    response = requests.get(image['url'])
    image_data = response.content

    # Create the folder if it doesn't exist
    os.makedirs(destination_path, exist_ok=True)

    # Extract the filename from the URL
    filename = str(image['created'])+".png"

    # Save the image to the specified folder
    image_path = os.path.join(destination_path, filename)
    with open(image_path, 'wb') as file:
        file.write(image_data)

    print(f"Image downloaded and saved at: {destination_path}")

# Provide the URL of the image you want to download
#image = dalle_create_img(prompt)

# Call the function to download the image to the specified folder
#download_image(image, destination_path)

def dalle_create_edit_img(image, mask, prompt):
    response=openai.Image.create_edit(
        image=open(image, "rb"),
        mask=open(mask, "rb"),
        prompt=prompt,
        n=2,
        size="256x256"
        )
    return{
        'url':response['data'][0]['url'], 
        'created':response['created']}
    
    
def dalle_create_variation(image):
    response=openai.Image.create_variation(
        image=open(image, "rb"),
        n=2,
        size="1024x1024"
        )
    return{
        'url':response['data'][0]['url'], 
        'created':response['created']}

#image="gen_images/1684235218.png"
#variation=dalle_create_variation(image)
#download_image(variation, destination_path)

def set_image_size(input_image_path, output_image_path, target_size):
    # Open the image using Pillow
    image = Image.open(input_image_path)

    # Resize the image to the target size while maintaining aspect ratio
    image.thumbnail(target_size, Image.ANTIALIAS)

    # Create a new image with a white background of the target size
    new_image = Image.new("RGBA", target_size, (255, 255, 255, 255))
    new_image.paste(image, ((target_size[0] - image.size[0]) // 2, (target_size[1] - image.size[1]) // 2))

    # Save the resized image
    new_image.save(output_image_path)

    print(f"Image resized and saved at: {output_image_path}")

# Set the target size for the image (256x256 pixels)
target_size = (256, 256)

image_path="images/scorcese_0.png"
mask_path="images/scorcese_mask.png"
prompt="put a face of a happy john lennon"


# Call the function to set the image size
set_image_size(image_path, image_path, target_size)
set_image_size(mask_path, mask_path, target_size)

edit_mask=dalle_create_edit_img(image_path,mask_path,prompt)
print(edit_mask)

created_img=dalle_create_img(prompt)
print(created_img)
