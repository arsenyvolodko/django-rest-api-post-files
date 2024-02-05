import time

import logging
from celery import shared_task
from .models import File
from mimetypes import guess_type

logger = logging.getLogger(__name__)


@shared_task
def process_file(file_id):
    file_instance = File.objects.get(id=file_id)
    file_path = file_instance.file.path
    mime_type, _ = guess_type(file_path)

    if not mime_type:
        process_unknown(file_path)
        mark_file_as_processed(file_instance)
        return

    if mime_type.startswith('image/'):
        process_image(file_path)
    elif mime_type.startswith('text/'):
        process_text(file_path)
    elif mime_type.startswith('video/'):
        process_video(file_path)
    elif mime_type.startswith('audio/'):
        process_audio(file_path)
    elif mime_type.startswith('application/'):
        process_application(file_path)
    else:
        process_unknown(file_path)

    mark_file_as_processed(file_instance)
    return file_id


def mark_file_as_processed(file_instance):
    file_instance.processed = True
    file_instance.save()


def process_image(file_path):
    logger.info(f'Processing image {file_path}')
    time.sleep(5)  # imitating image processing


def process_text(file_path):
    logger.info(f'Processing text {file_path}')
    time.sleep(3)  # imitating text processing


def process_video(file_path):
    logger.info(f'Processing video {file_path}')
    time.sleep(10)  # imitating video processing


def process_audio(file_path):
    logger.info(f'Processing audio {file_path}')
    time.sleep(7)  # imitating audio processing


def process_application(file_path):
    logger.info(f'Processing application {file_path}')
    time.sleep(7)  # imitating application processing


def process_unknown(file_path):
    logger.info(f'Processing unknown type file {file_path}')
    time.sleep(7)  # imitating unknown file processing
