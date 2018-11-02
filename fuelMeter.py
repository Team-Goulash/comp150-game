import pygame
import random

class Torch: # Change name later
    # Maximum torch time
    MAX_TORCH_TIME = 80
    # Torch time upon spawning
    torch_time = 50;
    # Bar images
    bar_holder = pygame.image.load("./UI/fuel_bar_holder.png")
    fuel_bar = pygame.image.load("./UI/fuel_bar.png")

    def reset_fuel(self):
        self.torch_time = 0
        self.add_fuel()

    def add_fuel(self):
        # Todo put fule range back to 20, 30
        fuel_reward = random.randint(60, 80)
        self.torch_time += fuel_reward
        print("added ", fuel_reward, "to your torch")

    def torch_extinguishing(self):
        pass

    def display_fuel_meter(self, surface, position):
        if self.torch_time <= 0:
            self.add_fuel()
        surface.blit(self.bar_holder, position)
        bar_width, bar_height = self.fuel_bar.get_size()
        temp_bar = pygame.transform.scale(self.fuel_bar, (int(bar_width * self.get_fuel_percentage()), bar_height))
        surface.blit(temp_bar, position)

    def get_fuel_percentage(self):
        return self.torch_time / self.MAX_TORCH_TIME

    def update_fuel_timer(self, delta_time):
        self.torch_time -= delta_time
