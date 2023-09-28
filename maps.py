import requests, pygame, sys, os
from math import pow

class MapParameters():
    'Класс создания параметров местоположения'
    def __init__(self, latitude = 37.480956, longitude = 55.669764, zoom = 16, size = '650,400'):
        self.latitude = latitude
        self.longitude = longitude
        self.zoom = zoom
        self.size = size
        self.type = "map"

    def ll(self):
        return str(str(self.latitude) + "," + str(self.longitude))
    
    def update(self, event, speed = 0.005, type = "map"):
        if event.scancode == 75 and self.zoom < 19:  # Page_UP
            self.zoom += 1
        elif event.scancode == 78 and self.zoom > 2:  # Page_DOWN
            self.zoom -= 1
        elif event.scancode == 81:  # LEFT_ARROW
            self.longitude -= speed * pow(2, 14 - self.zoom)
        elif event.scancode == 82:  # RIGHT_ARROW
            self.longitude += speed * pow(2, 14 - self.zoom)
        elif event.scancode == 79 and self.latitude < 85:  # UP_ARROW
            self.latitude += speed * pow(2, 15 - self.zoom)
        elif event.scancode == 80 and self.latitude > -85:  # DOWN_ARROW
            self.latitude -= speed * pow(2, 15 - self.zoom)  
        elif event.scancode == 25:  # v
            if self.type == "map":
                self.type = "sat"
            elif self.type == "sat":
                self.type = "sat,skl"
            elif self.type == "sat,skl":
                self.type = "map"

def map_creation(mymap):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&size={size}&l={type}".format(
        ll = mymap.ll(),
        z = mymap.zoom,
        size = mymap.size,
        type = mymap.type
    )
    response = requests.get(map_request)
    if not response:
        print("Connection error: " , response.status_code, response.reason)
    map_png = "map.png"
    try:
        with open(map_png, 'wb') as file:
            file.write(response.content)
    except IOError as exeption:
        print("Writing file error: ", exeption)
    return map_png

def main():
    pygame.init()
    # print("Введите три строки: широту, долготу и приближение")
    # lat = input()
    # lon = input()
    # zoom = input()
    map = MapParameters()#lat, lon, zoom)#при желании можно ввести свои координаты
    screen = pygame.display.set_mode((650,400))
    while(True):
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            map.update(event)
        map_png = map_creation(map)
        screen.blit(pygame.image.load(map_png), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_png)

if __name__ == "__main__":
    main()
