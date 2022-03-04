from os import walk
import pygame

def import_audio(path):
    audio_batch = []
    for _, __, mp3_files in walk(path):
        for mp3 in mp3_files:
            full_path = path + '/' + mp3
            try:
                audio_batch.append(pygame.mixer.Sound(full_path))
            except Exception as e:
                print(e)


    return audio_batch