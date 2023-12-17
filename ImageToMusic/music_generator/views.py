import zipfile
from io import BytesIO

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from .music_generator import generate_music_from_image


def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)

        # Call the music generation function with the uploaded image
        audio_file_path, midi_file_path = generate_music_from_image(filename)

        # Create a zip file containing both the audio and MIDI files in memory
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            zip_file.write(audio_file_path, 'generated_audio.wav')
            zip_file.write(midi_file_path, 'generated_music.mid')

        # Seek to the beginning of the buffer before returning its data
        zip_buffer.seek(0)

        # Create a response with the zip file
        response = HttpResponse(zip_buffer.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="generated_music.zip"'

        return response

    return render(request, 'upload_image.html')
