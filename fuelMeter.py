import pygame
import random
import library

class Torch: # Change name later
    # Maximum torch time
    MAX_TORCH_TIME = 80
    START_TORCH_TIME_MULTIPLIER = 0.75
    # Torch time upon spawning
    torch_time = MAX_TORCH_TIME * START_TORCH_TIME_MULTIPLIER
    # Bar images
    bar_holder = pygame.image.load("./UI/fuel_bar_holder.png")
    fuel_bar = pygame.image.load("./UI/fuel_bar.png")

    def reset_fuel(self):
        self.torch_time = self.MAX_TORCH_TIME * self.START_TORCH_TIME_MULTIPLIER
        print("reset time ", self.torch_time)

    def add_fuel(self):
        # Todo put fule range back to 20, 30
        fuel_reward = random.randint(20, 30)
        self.torch_time += fuel_reward
        self.torch_time = library.clamp(0, self.MAX_TORCH_TIME, self.torch_time)
        print("added ", fuel_reward, "to your torch")

    def torch_extinguishing(self):
        pass

    def display_fuel_meter(self, surface, position):
        if self.torch_time <= 0:
            self.torch_time = 0
        surface.blit(self.bar_holder, position)
        bar_width, bar_height = self.fuel_bar.get_size()
        temp_bar = pygame.transform.scale(self.fuel_bar,
                                          (int(bar_width * self.get_fuel_percentage()), bar_height)
                                          )
        surface.blit(temp_bar, position)

    def get_fuel_percentage(self):
        return self.torch_time / self.MAX_TORCH_TIME

    def update_fuel_timer(self, delta_time):
        self.torch_time -= delta_time
