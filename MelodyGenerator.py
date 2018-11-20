import pygame
import sys
import wave
import math
import struct
import random
from pygame.locals import *

pygame.init()
pygame.display.set_mode((250, 250), 0, 32)


class MusicGenerator:
    filename = "song.wav"
    wav_write = wave.open(filename, 'w')
    wav_write.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))

    values = []
    SAMPLE_RATE = wav_write.getframerate()

    D_MINOR = {"D": 587.33, "E": 659.25, "F": 698.46, "G": 783.99, "A": 880.00,
               "Bflat": 932.33, "C": 1046.50}
    D_MINOR_CHORD_A = [D_MINOR["A"], D_MINOR["F"], D_MINOR["D"]]
    D_MINOR_CHORD_B = [D_MINOR["Bflat"], D_MINOR["G"], D_MINOR["E"]]
    D_MINOR_CHORD_C = [D_MINOR["C"], D_MINOR["A"], D_MINOR["F"]]
    D_MINOR_CHORD_D = [D_MINOR["D"], D_MINOR["Bflat"], D_MINOR["G"]]
    D_MINOR_CHORD_E = [D_MINOR["E"], D_MINOR["C"], D_MINOR["A"]]
    D_MINOR_CHORD_F = [D_MINOR["F"], D_MINOR["D"], D_MINOR["Bflat"]]
    D_MINOR_CHORD_G = [D_MINOR["G"], D_MINOR["E"], D_MINOR["C"]]

    D_MINOR_CHORDS = {1: D_MINOR_CHORD_A, 2: D_MINOR_CHORD_B, 3: D_MINOR_CHORD_C, 4: D_MINOR_CHORD_D,
                      5: D_MINOR_CHORD_E, 6: D_MINOR_CHORD_F, 7: D_MINOR_CHORD_G}

    current_chord = 1
    frequency = random.choice(D_MINOR_CHORDS[current_chord])
    frequency2 = random.choice(D_MINOR_CHORDS[current_chord]) * 2
    snare_freq = 1
    hi_hat_freq = 1
    currentProgress = 0
    currentNote = 2
    currentNote2 = 0
    multiplier = 10
    songRate = SAMPLE_RATE * multiplier
    volume = 0
    threshold = 0.1

    def chord_progression(self, i):
        if i >= self.songRate * self.threshold:
            self.threshold += 0.1
            if self.current_chord < len(self.D_MINOR_CHORDS.values()):
                self.current_chord += 3
            else:
                self.current_chord = 1
        print(self.threshold)

    def snare(self):
        snare_speed = 20
        if self.currentNote == 4:
            self.snare_freq = random.randint(100, 1000)
            if self.currentProgress == self.songRate / (snare_speed
                                                        * self.multiplier):
                self.snare_freq = 1
                self.currentNote = 0

    def hi_hat(self):
        hi_hat_speed = 150
        if self.currentNote2 == 1:
            self.hi_hat_freq = random.randint(5000, 10000)
            if self.currentProgress == self.songRate / (hi_hat_speed
                                                        * self.multiplier):
                self.hi_hat_freq = 1
                self.currentNote2 = 0

    def melody(self):
        tempo = 10
        if self.currentProgress == self.songRate / (tempo * self.multiplier):
            self.frequency = random.choice(self.D_MINOR_CHORDS[self.current_chord])
            self.frequency2 = random.choice(self.D_MINOR_CHORDS[self.current_chord]) * 2
            self.currentNote += 1
            self.currentNote2 += 1
            self.currentProgress = 0

    def create_value(self, i, frequency, volume):
        max_sample_value = 2**15 - 1
        sample_value = math.sin(
            2.0 * math.pi * frequency * (
                    i / float(self.SAMPLE_RATE))) * (
                    volume * max_sample_value)
        return sample_value

    def fade_out(self, i):
        if i >= self.songRate * 0.9:
            if self.volume > 0:
                self.volume -= 0.00005

    def fade_in(self):
            if self.volume <= 0.9:
                self.volume += 0.000005

    def generate_track(self):
        for i in range(0, self.songRate):
            self.currentProgress += 1

            self.fade_in(self)
            self.chord_progression(self, i)
            self.snare(self)
            self.hi_hat(self)
            self.melody(self)
            self.fade_out(self, i)

            sample_value = self.create_value(self, i, self.frequency, self.volume / 4)
            sample_value2 = self.create_value(self, i, self.frequency2,
                                              self.volume / 4)
            sample_value3 = self.create_value(self, i, self.snare_freq, self.volume / 4)
            sample_value4 = self.create_value(self, i, self.hi_hat_freq, self.volume / 4)

            print(sample_value + sample_value2 + sample_value3 + sample_value4)
            packed_value = struct.pack('i', int(sample_value + sample_value2 + sample_value3 + sample_value4))

            for j in range(0, self.wav_write .getnchannels()):
                self.values.append(packed_value)

        value_str = b"".join(self.values)
        self.wav_write.writeframesraw(value_str)

        self.wav_write.close()


MusicGenerator.generate_track(MusicGenerator)
sound = pygame.mixer.Sound(MusicGenerator.filename)
pygame.mixer.Sound.set_volume(sound, 100)


def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    sound.stop()
                    sound.play()


if __name__ == "__main__":
    main()
