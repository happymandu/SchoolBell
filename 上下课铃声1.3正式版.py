import pandas as pd  
import pygame  
from datetime import datetime  
import os
import threading
import sys  
new_working_directory = 'D:/time/上下课铃声'  
os.chdir(new_working_directory)  
current_working_directory = os.getcwd()  
pygame.init() 
pygame.mixer.init() 
exit_flag = False
SCREEN_WIDTH = 250  
SCREEN_HEIGHT = 50  
FONT = pygame.font.Font('C:\Windows\Fonts\STKAITI.TTF', 24)
WHITE = (255, 255, 255)  
RED = (255, 0, 0)  
GREEN = (0, 255, 0)  
def read_schedule_from_csv(file_path):  
    df = pd.read_csv(file_path, encoding='ANSI')  
    schedule = {}  
    for index, row in df.iterrows():  
        scheduled_time = datetime.strptime(row['Time'], '%H:%M:%S').time()  
        sound_file = row['SoundFile']  
        schedule[scheduled_time] = sound_file  
    return schedule  
def check_and_play_sound(schedule):  
    global exit_flag
    while not exit_flag:
        now = datetime.now()  
        current_time_str = now.strftime('%H:%M:%S')  
        for scheduled_time_obj, sound_file in schedule.items():
            scheduled_time_str = scheduled_time_obj.strftime('%H:%M:%S')  
            if current_time_str == scheduled_time_str:  
                play_sound(sound_file)  
                break 
        if not exit_flag:
            pygame.time.wait(100)
def play_sound(sound_file):  
    try:  
        pygame.mixer.music.load(sound_file)  
        pygame.mixer.music.play()  
        while pygame.mixer.music.get_busy():  
            pygame.time.Clock().tick(10)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
def create_ui(schedule):  
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  
    pygame.display.set_caption("铃声播放器")  
    clock = pygame.time.Clock()  
    threading.Thread(target=check_and_play_sound, args=(schedule,)).start()
    while True:  
        global exit_flag
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  
        pygame.display.set_caption("铃声播放器")  
        clock = pygame.time.Clock()  
        thread = threading.Thread(target=check_and_play_sound, args=(schedule,))
        thread.daemon = True
        thread.start()
        while not exit_flag:  
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    exit_flag = True
                    pygame.quit()  
            if not exit_flag:
                screen.fill(WHITE)  
                current_time_str = datetime.now().strftime('%H:%M:%S')  
                current_time_text = FONT.render(f"当前时间: {current_time_str}", True, RED)  
                screen.blit(current_time_text, (10, 10))  
                pygame.display.flip()  
                clock.tick(60) 
                pygame.display.flip()
            else:
                pygame.quit()
                sys.exit()
def main():  
    csv_file_path = 'time.csv'  
    schedule = read_schedule_from_csv(csv_file_path)  
    create_ui(schedule)  
if __name__ == '__main__':  
    main()  