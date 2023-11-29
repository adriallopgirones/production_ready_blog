from celery import shared_task
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from PIL import Image

from core_apps.users.models import PublicProfile


@shared_task
def process_and_save_profile_picture(profile_id, image_data):
    try:
        public_profile = PublicProfile.objects.get(id=profile_id)

        # Image processing, we can resize it for example
        img = Image.open(image_data)
        img = img.resize((300, 300))

        # Save the processed image to a temporary file
        temp_file = NamedTemporaryFile(delete=True)
        img.save(temp_file, format="JPEG")

        # Save the processed image to the profile_picture field
        public_profile.profile_picture.save(
            f"profile_picture_{profile_id}.jpg", File(temp_file)
        )

        # Clean up the temporary file
        temp_file.close()
    except PublicProfile.DoesNotExist:
        print(
            f"Profile with id {profile_id} does not exist, could not save profile picture"
        )
