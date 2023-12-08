import pygame
import random
import copy
from button import Button
import sys
import json





tetris_logo = pygame.image.load("img/tetris_logo.png")

tetris_logo_new = pygame.transform.scale(tetris_logo, (tetris_logo.get_width() // 2, tetris_logo.get_height() // 2))
tetris_logo_rect = tetris_logo_new.get_rect(center=(610,100))
bg1 = pygame.image.load("img/bg1.png")
bg1_rect = bg1.get_rect()
bg1_rect.topleft = 0,0
music = False
button_img = pygame.image.load("img/button.png")
new_button_img = pygame.transform.scale(button_img, (300,100))
music_btn = pygame.transform.scale(button_img, (100,100))
transformed_img = pygame.transform.scale(button_img, (200,70))








def game_loop():
    pygame.init()
    pygame.mixer.music.stop()
    diktak = {"a":0}
    if diktak["a"]:
        print("joo")

    W = 10
    H = 18
    TILE = 45
    RES = 750, 940
    GAME_RES = W * TILE, H * TILE
    MOVE_SHAPE = pygame.USEREVENT + 1
    TIMER = pygame.USEREVENT + 2
    speed = 150
    pygame.time.set_timer(MOVE_SHAPE, speed)
    pygame.time.set_timer(TIMER, 3000)
    surface = pygame.display.set_mode(RES)
    screen = pygame.Surface(GAME_RES)
    music_coll = pygame.mixer.Sound("media/collide.wav")
    move_music = pygame.mixer.Sound("media/ditak.wav")   
    box = False
    
    stop = False   
    current_speed = speed
    shape_num = 0  
    score = 0
    pause_set = False
    game_over = False
    current_score = score
    warning = False
    

    grid = []

    for y in range(H):
        for x in range(W):
            rect = pygame.Rect(x * TILE, y * TILE, TILE, TILE)
            grid.append(rect)


    figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                [(0, 0), (0, -1), (0, 1), (-1, -1)],
                [(0, 0), (0, -1), (0, 1), (1, -1)],
                [(0, 0), (0, -1), (0, 1), (-1, 0)]]

    colors = ["blue", "red", "green", "yellow", "pink", "orange", "white"]


    shapes = []


    def add_shape():
        
        random_num = random.randint(0, 6)
        shape = figures_pos[random_num]
        rect_list = []
        for i in shape:
            rect = pygame.Rect(i[0] * TILE + 180, i[1] * TILE + 90, TILE, TILE)
            rect_list.append(rect)
        
            
            
        
        shapes.append(rect_list)
        

        

            
    def collides_shapes(shape1, shape2):
        return shape1.y == shape2.y - TILE and shape1.x == shape2.x

    def collides_shapes2(shape1, shape2):
        return shape1.y == shape2.y and shape1.x == shape2.x - TILE

    def collides_shapes3(shape1, shape2):
        return shape1.y == shape2.y and shape1.x == shape2.x + TILE

        

    def check_line(shapes):
        my_arr = []
        count_dict = {}
        finished_arr = []

        for shape in shapes:
            for rect in shape:
                
                row = int(rect.y)
                my_arr.append(row)
        
        for y in my_arr:
            if y not in count_dict:
                count_dict[y] = 1
            else:
                count_dict[y] += 1

        
        most_common_nums = [k for k, v in count_dict.items() if v == 10]
        
        for one in most_common_nums:
            
            finished_arr.append(one)
        print(count_dict)
        
            
                
        return finished_arr
    
                        
                    
    def check_borders(shape):
        for rect in shape:
            if rect.x > W * TILE - 1 or rect.x < 0 or rect.y > H * TILE - 1:
                return True
            
        return False

    def check_game_over(shapes):
        for shape in shapes[:-1]:
            for rect in shape:
                if rect.y <= TILE:
                    return True
        return False

    def score_plus(fulfilled_lines):
        vysledek = 1 * (fulfilled_lines * 1) * fulfilled_lines
        return vysledek
    
    def set_record():
        
        
        try:
            with open("player_scores.json", "r") as file:
                board_of_leaders = json.load(file)
        except FileNotFoundError:
            board_of_leaders = {}
        
        
        if len(board_of_leaders) < 7:
            if user_text in board_of_leaders:
                pass
            else:
                board_of_leaders[user_text] = current_score
                
        else:
            lowest_score = min(board_of_leaders.values())
            players_to_remove = []
            for name, score in board_of_leaders.items():
                if score == lowest_score:
                    players_to_remove.append(name)
            for name in players_to_remove:
                del board_of_leaders[name]
            if user_text in board_of_leaders:
                pass
                
            else:
                board_of_leaders[user_text] = current_score   
                    

        
        
        provisory_board = {}    
        
        while len(board_of_leaders):
            loop_board = board_of_leaders.copy()
            max_value = max(loop_board.values())
            for key,value in loop_board.items():
                
                if value == max_value:
                    provisory_board[key] = value
                    del board_of_leaders[key]              
                    
        
        board_of_leaders = provisory_board


        
        with open("player_scores.json", "w") as file:
            json.dump(board_of_leaders, file)

       


    font = pygame.font.SysFont("calibri", 40, bold=True)
    text_score = font.render(f"SCORE: {score}", True, "white")
    text_score_rect = text_score.get_rect()
    text_score_rect.topleft = 535, 240 

    

    add_shape()
    add_shape()
    

    run = True
    while run:
        
        
        event_list = pygame.event.get()
        
        myska = pygame.mouse.get_pos()
        
        
        if pause_set:
            pause_font = pygame.font.SysFont("calibri", 80, bold=True)
            text = pause_font.render("PAUSED", True, "white")
            text_rect = text.get_rect()
            text_rect.midtop =  222, 350

            screen.blit(text, text_rect)
        
        if game_over:
            
            stop = True
            pygame.time.set_timer(MOVE_SHAPE, 0)
            text_score_rect.topleft = 2000, 300
            
            mouse_pos = pygame.mouse.get_pos()
            text_got_score = font.render(f"Your score is: {current_score}", True, "white")
            text_got_score_rect = text_got_score.get_rect(center=(222, 250))
            button_menu = Button((230,350), new_button_img, "GO TO MENU", font, "black", "red")
            button_set_record = Button((230,500), new_button_img, "SET RECORD", font, "black", "red")
            button_send = Button((230,730), transformed_img, "SET", font, "black", "red")
            
            

            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN:
                
                    if button_menu.check_for_input(mouse_pos):
                        menu()
                    
                    if button_set_record.check_for_input(mouse_pos):
                        board_of_leaders = {}
                        
                         
                        user_text = ""
                        box = True
                        
                        
                        
                        if box:
                            text_box = pygame.Rect(80,600,300,60)

                            for event in event_list:
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    
                                    if text_box.collidepoint(myska):
                                        zezo = True

                                    else:
                                        zezo = False
                                if event.type == pygame.KEYDOWN:
                                    
                                    if zezo:
                                        if event.key == pygame.K_BACKSPACE:
                                            user_text = user_text[:-1]
                                        elif len(user_text) < 10:
                                            user_text += event.unicode
                                            print(user_text)
                                            
                            if zezo:
                                color = pygame.Color("yellow")
                            else:
                                color = pygame.Color("white")
                            
                            pygame.draw.rect(screen, color, text_box, 4)
                            user_input = font.render(user_text, True, "white")
                            screen.blit(user_input,(text_box.x + 10, text_box.y +10))

                            button_send.change_color(myska)
                            button_send.update(screen)
                            
                            


                    if button_send.check_for_input(mouse_pos):
                        try:
                            with open("player_scores.json", "r") as file:
                                hraci_dict = json.load(file)
                        except FileNotFoundError:
                                hraci_dict = {}
                        if hraci_dict.get(user_text) is None: 
                            set_record()
                            menu()
                            warning = False
                        else:
                            warning = True
                
                        
            
                    
                        
            
            if box:
                
                text_box = pygame.Rect(80,600,300,60)
        
                for event in event_list:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        
                        if text_box.collidepoint(myska):
                            zezo = True

                        else:
                            zezo = False
                    if event.type == pygame.KEYDOWN:
                        if zezo:
                            if event.key == pygame.K_BACKSPACE:
                                user_text = user_text[:-1]
                            elif len(user_text) < 10:
                                user_text += event.unicode
                if zezo:
                    color = pygame.Color("yellow")
                else:
                    color = pygame.Color("white")
                
                pygame.draw.rect(screen, color, text_box, 4)
                user_input = font.render(user_text, True, "white")
                screen.blit(user_input,(text_box.x + 10, text_box.y +10))

                button_send.change_color(myska)
                button_send.update(screen)
                
                    

            for button in [button_menu, button_set_record]:
                button.change_color(myska)
                button.update(screen)
                
            
            screen.blit(text_got_score, text_got_score_rect)
            pygame.display.flip()
               
        surface.blit(bg1, bg1_rect)
        
        surface.blit(screen, (20, 20))
        screen.fill("#171717")
        
        next_shape = copy.deepcopy(shapes[-1])
        
       

        for event in event_list:
            
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            if event.type == pygame.KEYUP:
                    pygame.time.set_timer(MOVE_SHAPE, current_speed)
            
            

            if event.type == MOVE_SHAPE:
                
                
                
                
                collides_with_grid = any(shape.y >= (H*TILE) - TILE for shape in shapes[shape_num])
                collides_with_shape = False
                
                for rect in shapes[shape_num]:
                    for i in range(shape_num):
                        for rect2 in shapes[i]:
                        
                            if collides_shapes(rect, rect2):
                                collides_with_shape = True

                
                if collides_with_grid or collides_with_shape:
                    
                    if check_game_over(shapes):
                        
                        
                        game_over = True
                        if game_over:
                            current_speed = 0

                        else:
                            current_speed = speed

                        font_over = pygame.font.SysFont("calibri", 80, bold=True)
        
                        text2 = font_over.render("GAME OVER", True, "white")
                        text2_rect = text2.get_rect()
                        text2_rect.midtop =  220, 350
                        
                            
                        
                    
                    fulfilled_lines = check_line(shapes)
                    current_score += score_plus(len(fulfilled_lines))
                    text_score = font.render(f"SCORE: {current_score}", True, "white")
                    
                    
                    

                    
                    if len(fulfilled_lines) > 0:
                        if music:
                            music_coll.play()

                        
                        
                        for shape in shapes:
                            new_shapes = []
                            for rect in shape:
                                if rect.y not in fulfilled_lines:
                                    new_shapes.append(rect)

                            shape.clear()
                            shape.extend(new_shapes)
                        

                        
                            
                                    
                    
                        for shape in shapes:
                            for rect in shape:
                                for line in fulfilled_lines:
                                    if rect.y < line:
                                        rect.y += (len(fulfilled_lines) * TILE)


                    add_shape()
                    
                    shape_num += 1  
                        
                    
                    for shape in shapes[shape_num]:
                        grid.append(shape)       
                    

                else:
                    for shape in shapes[shape_num]:
                        shape.y += TILE
                    
                    

            if event.type == pygame.KEYDOWN:
                if not stop:
                    if event.key == pygame.K_SPACE:
                    
                        
                        pause_set = not pause_set
                    
                    if pause_set:
                        current_speed = 0
                    else:
                        current_speed = speed

        
                if event.key == pygame.K_a:
                    
                    if not any(rect.x < 45 for rect in shapes[shape_num]):
                        moving = True
                        for rectangle in shapes[shape_num]:
                            for i in range(shape_num):
                                for rect2 in shapes[i]:
                        
                                    
                                    if collides_shapes3(rectangle, rect2):
                                        moving = False
                                        
                                if not moving:
                                    break
                                    
                    else:
                        moving = False

                    if moving: 
                        if not pause_set and not game_over:                           
                            for jama in shapes[shape_num]:
                                jama.x -= TILE
            

                if event.key == pygame.K_d:
                    
                    
                    if not any(rect.x > 400 for rect in shapes[shape_num]):
                        can_move = True
                        for rectangle in shapes[shape_num]:
                            for i in range(shape_num):
                                for rect2 in shapes[i]:
                        
                                    
                                    if collides_shapes2(rectangle, rect2):
                                        can_move = False
                                        
                                if not can_move:
                                    break
                                    
                    else:
                        can_move = False

                    if can_move:
                        if not pause_set and not game_over:                            
                            for jama in shapes[shape_num]:
                                jama.x += TILE

                    

                if event.key == pygame.K_w:
                    if not stop:
                        if music:
                            move_music.play()
                        if not pause_set:
                            old_shape = copy.deepcopy(shapes[shape_num])
                            center = shapes[shape_num][0]
                            for i in range(4):
                                x = shapes[shape_num][i].y - center.y
                                y = shapes[shape_num][i].x - center.x
                                shapes[shape_num][i].x = center.x - x
                                shapes[shape_num][i].y = center.y + y

                            if check_borders(shapes[shape_num]):
                                shapes[shape_num] = old_shape


                keys = pygame.key.get_pressed()
                if keys[pygame.K_s]:
                    pygame.time.set_timer(MOVE_SHAPE, 40)

                   



        for i_rect in grid:
            pygame.draw.rect(screen, (40,40,40), i_rect, 1)


        
        if not pause_set and not game_over:
            for i, shape in enumerate(shapes[:-1]):
                for rect in shape:
                    pygame.draw.rect(screen, colors[i % len(colors)], rect)
                    pygame.draw.rect(screen, "black", rect, 1)

            
            for rect2 in next_shape:
                rect2.x += 430
                rect2.y += 300
                pygame.draw.rect(surface, colors[(len(shapes) - 1) % len(colors)], rect2)
                pygame.draw.rect(surface, "black", rect2, 1)
        if warning:
            warn_font = pygame.font.SysFont("calibri", 22)
            warn_text = warn_font.render("Nickname already exists. Choose another one.", True, "red")  
            warn_text_rect = warn_text.get_rect(center=(230, 570)) 
            screen.blit(warn_text,warn_text_rect) 



            
                
        
        surface.blit(tetris_logo_new, tetris_logo_rect)
        surface.blit(text_score, text_score_rect)
        pygame.display.update()


def leaderboard():
    
    pygame.init()
    

    RES = 750, 940
    board_screen = pygame.display.set_mode(RES)
    pygame.display.set_caption("Tetris")
    

    font = pygame.font.SysFont("calibri", 40, bold=True)
    
    
    button_img = pygame.image.load("img/button.png")
    new_button_img = pygame.transform.scale(button_img, (300,70))
    
    def get_record():
        y = 40
        name_record = []
        score_record = []

        headline_text = font.render("PLACE                  NICK                   SCORE", True, "yellow")
        headline_text_rect = headline_text.get_rect(center=(365, 40))
        board_screen.blit(headline_text, headline_text_rect)

        with open("player_scores.json", "r") as file:
                board_of_leaders = json.load(file)
        
        for name, score in board_of_leaders.items():
            name_record.append(name)
            score_record.append(score)



        for i in range(len(name_record)):
            y += 100
            name = name_record[i]
            score = score_record[i]
            name_text = font.render(f"{name}", True, "white")
            name_text_rect = name_text.get_rect(center=(350,y))
            board_screen.blit(name_text, name_text_rect)
            score_text = font.render(f"{score}", True, "white")
            score_text_rect = score_text.get_rect(center=(625,y))
            board_screen.blit(score_text, score_text_rect)
            place_text = font.render(f"{i + 1}", True, "white")
            place_text_rect = place_text.get_rect(center=(100,y))
            board_screen.blit(place_text, place_text_rect)



    running = True
    while running:
        
        mouse_pos = pygame.mouse.get_pos()
        button_back = Button((170, 850), new_button_img, "BACK", font, "black", "red")
        board_screen.fill("black")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.check_for_input(mouse_pos):
                    menu()

        
        board_screen.blit(bg1,(0,0))
        
        button_back.change_color(mouse_pos)
        button_back.update(board_screen)
        get_record()
        pygame.display.update()




def menu():
    
    
    pygame.init()
    
    pygame.mixer.music.load("media/menu.wav")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.2)
    RES = 750, 940
    menu_screen = pygame.display.set_mode(RES)
    pygame.display.set_caption("Tetris")
    font = pygame.font.SysFont("calibri", 40, bold=True)
    sound_on_img = pygame.image.load("img/on.png")
    sound_off_img = pygame.image.load("img/off.png")
    new_sound_on_img = pygame.transform.scale(sound_on_img, (80,80))
    new_sound_off_img = pygame.transform.scale(sound_off_img, (80,80))
    
    def rect_music(music):
        if not music:
            rect = pygame.Rect(420 ,755, 90, 95)
            return rect
        else:
            rect2 = pygame.Rect(240 ,755, 90, 95)
            return rect2

    go = True
    while go:

        
        
        global music
        if music:
            pygame.mixer.music.set_volume(0.3)
        else:
            pygame.mixer.music.set_volume(0.0)

        mouse_pos = pygame.mouse.get_pos()
        button1 = Button((RES[0]//2,350), new_button_img, "PLAY", font, "black", "red")
        button2 = Button((RES[0]//2,500), new_button_img, "LEADERBOARD", font, "black", "red")
        button3 = Button((RES[0]//2,650), new_button_img, "QUIT", font, "black", "red")
        button4 = Button(((RES[0]//2) -90,800), music_btn, "", font, "black", "red")
        button5 = Button(((RES[0]//2) +90,800), music_btn, "", font, "black", "red")
        menu_screen.fill("black")
        rect = rect_music(music)
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                go = False
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if button1.check_for_input(mouse_pos):
                    game_loop()
                    
                if button2.check_for_input(mouse_pos):
                    leaderboard()
                if button3.check_for_input(mouse_pos):
                    go = False
                    sys.exit()

                if button4.check_for_input(mouse_pos):
                    music = True
                    
                    

                if button5.check_for_input(mouse_pos):
                    music = False
        
        menu_screen.blit(bg1, (0,0))
        menu_screen.blit(tetris_logo, (190, 100))
        
        for button in [button1, button2, button3, button4, button5]:
            button.change_color(mouse_pos)
            button.update(menu_screen)

        menu_screen.blit(new_sound_on_img,((RES[0]//2) -133,763))  
        menu_screen.blit(new_sound_off_img,((RES[0]//2) +50,763))
        pygame.draw.rect(menu_screen, "green",rect, 4)
            
        pygame.display.update()

menu()
