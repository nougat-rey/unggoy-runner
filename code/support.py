from os import walk
import pygame


def import_audio(path):
    audio_batch = []
    for _, __, audio_files in walk(path):
        for audio in audio_files:
            full_path = path + '/' + audio
            try:
                audio_batch.append(pygame.mixer.Sound(full_path))
            except Exception as e:
                print(e)

    return audio_batch
