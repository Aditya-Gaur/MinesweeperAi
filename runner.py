import pygame
import sys
import time

from minesweeper import Minesweeper, MinesweeperAI

HEIGHT = 8
WIDTH = 8
MINES = 8


# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

pygame.init()
size = width, height = 600, 400
selected = ()

# Fonts
OPEN_SANS = "assets/fonts/Koulen-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 22)
mediumFont = pygame.font.Font(OPEN_SANS, 30)
largeFont = pygame.font.Font(OPEN_SANS, 40)


# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)


# Add images
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/mine.jpg")
mine = pygame.transform.scale(mine, (cell_size, cell_size))
bg = pygame.image.load("assets/images/bg.jpg")
bg = pygame.transform.scale(bg, (600, 400))


# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
lost = False

# Show instructions initially
instructions = True

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                instructions = True

    # Show game instructions
    if instructions:
        solvei = False

        # Create game
        screen = pygame.display.set_mode(size)
        screen.fill(BLACK)
        
        # Background
        screen.blit(bg, (0,0))

        # Title
        title = largeFont.render("Play Minesweeper", True, (255,255,102))
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Rules
        rules = [
            "Click a cell to reveal it.",
            "Right-click a cell to mark it as a mine."
        ]
        for i, rule in enumerate(rules):
            line = smallFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)

        # Play game button
        buttonRect = pygame.Rect((width / 4), (3 / 5) * height, width / 2, 50)
        buttonText = mediumFont.render("Play Game", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # Solve board button
        tbuttonRect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
        tbuttonText = mediumFont.render("Solve board", True, BLACK)
        tbuttonTextRect = tbuttonText.get_rect()
        tbuttonTextRect.center = tbuttonRect.center
        pygame.draw.rect(screen, WHITE, tbuttonRect)
        screen.blit(tbuttonText, tbuttonTextRect)

        # Check if either button clicked
        click, _, _ = pygame.mouse.get_pressed()
        beta_mode = False
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if tbuttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)
                solvei = True

            elif buttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)

                # Create game and AI agent
                HEIGHT = WIDTH = MINES = 8 
                game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
                revealed = set()
                flags = set()
                lost = False

        pygame.display.flip()
        continue
    
    if solvei:
        screen.fill(BLACK)

        title_text = largeFont.render("Board Configuration", True, (255,255,102))
        screen.blit(title_text, ((width / 2 - title_text.get_width() / 2), (height / 22)))

        help_text = smallFont.render("Press ENTER to continue", True, (137, 207, 240))
        screen.blit(help_text, ((width / 2 - help_text.get_width() / 2 -10), (height / 1.3)))

        # Get height and width and mines
        height_text = mediumFont.render("Height", True, WHITE)
        screen.blit(height_text, ((width / 2.5 - height_text.get_width() / 2), (height / 3.2)))

        width_text = mediumFont.render("Width", True, WHITE)
        screen.blit(width_text, ((width / 2.5 - width_text.get_width() / 2), (height / 2.45)))

        mines_text = mediumFont.render("Mines", True, WHITE)
        screen.blit(mines_text, ((width / 2.5 - mines_text.get_width() / 2), (height / 2)))

        height_box = pygame.Rect(width / 2.5 - height_text.get_width() / 2 + 110, height / 2.85, 30, 25)
        width_box = pygame.Rect(width / 2.5 - height_text.get_width() / 2 + 110, height / 2.245, 30, 25)
        mines_box = pygame.Rect(width / 2.5 - height_text.get_width() / 2 + 110, height / 1.85, 30, 25)

        screen.fill(WHITE, height_box)
        screen.fill(WHITE, width_box)
        screen.fill(WHITE, mines_box)

        run = True
        h_C = False
        w_C = False
        m_C = False
        while run:
            for even in pygame.event.get():

                if even.type == pygame.QUIT:
                    sys.exit()
                elif even.type == pygame.KEYDOWN:
                    if even.key == pygame.K_ESCAPE:
                        instructions = True
                        run = False
                    elif even.key == pygame.K_RETURN:
                        run = False
                        solvei = False
                        game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                        ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
                        revealed = set()
                        flags = set()
                        lost = False
                        beta_mode = True

                # Flashy red lines on hover
                if not h_C:
                    if height_box.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(screen, (220, 20, 60), height_box, 3)
                    else:
                        pygame.draw.rect(screen, WHITE, height_box, 3)

                if not w_C:
                    if width_box.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(screen, (220, 20, 60), width_box, 3)
                    else:
                        pygame.draw.rect(screen, WHITE, width_box, 3)

                if not m_C:
                    if mines_box.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(screen, (220, 20, 60), mines_box, 3)
                    else:
                        pygame.draw.rect(screen, WHITE, mines_box, 3)

                # Check clicks
                if even.type == pygame.MOUSEBUTTONDOWN:
                    if height_box.collidepoint(pygame.mouse.get_pos()):
                        h_C = True
                        w_C = False
                        m_C = False
                        pygame.draw.rect(screen, WHITE, width_box, 3)
                        pygame.draw.rect(screen, WHITE, mines_box, 3)

                        pygame.draw.rect(screen, (220, 20, 60), height_box, 3)
                    elif width_box.collidepoint(pygame.mouse.get_pos()):
                        w_C = True
                        h_C = False
                        m_C = False
                        pygame.draw.rect(screen, WHITE, height_box, 3)
                        pygame.draw.rect(screen, WHITE, mines_box, 3)

                        pygame.draw.rect(screen, (220, 20, 60), width_box, 3)
                    elif mines_box.collidepoint(pygame.mouse.get_pos()):
                        m_C = True
                        h_C = False
                        w_C = False
                        pygame.draw.rect(screen, WHITE, height_box, 3)
                        pygame.draw.rect(screen, WHITE, width_box, 3)

                        pygame.draw.rect(screen, (220, 20, 60), mines_box, 3)
                    else:
                        h_C = False
                        w_C = False
                        m_C = False
                        pygame.draw.rect(screen, WHITE, height_box, 3)
                        pygame.draw.rect(screen, WHITE, width_box, 3)
                        pygame.draw.rect(screen, WHITE, mines_box, 3)

                # Check for keyboard movements and record them
                if h_C or w_C or m_C:
                    if even.type == pygame.KEYDOWN:
                        if even.key == pygame.K_BACKSPACE:
                            try:
                                if h_C:
                                    HEIGHT = int(str(HEIGHT)[:-1])
                                elif w_C:
                                    WIDTH = int(str(WIDTH)[:-1])
                                elif m_C:
                                    MINES = int(str(MINES)[:-1])
                            except:
                                if h_C:
                                    HEIGHT = ""
                                elif w_C:
                                    WIDTH = ""
                                elif m_C:
                                    MINES = ""
                        try:
                            if int(even.unicode) in range(0, 10):
                                if h_C:
                                    HEIGHT = int(str(HEIGHT) + even.unicode)
                                elif w_C:
                                    WIDTH = int(str(WIDTH) + even.unicode)
                                elif m_C:
                                    MINES = int(str(MINES) + even.unicode)
                        except:
                            pass
                
                    screen.fill(BLACK, height_box)
                    screen.fill(BLACK, width_box)
                    screen.fill(BLACK, mines_box)
                    hei = mediumFont.render(str(HEIGHT), 1, BLACK)
                    wid = mediumFont.render(str(WIDTH), 1, BLACK)
                    mi = mediumFont.render(str(MINES), 1, BLACK)

                    height_box = pygame.Rect(width / 2.5 - height_text.get_width() / 2 + 110, height / 2.85, hei.get_width() + 10, 25)
                    width_box = pygame.Rect(width / 2.5 - height_text.get_width() / 2 + 110, height / 2.245, wid.get_width() + 10, 25)
                    mines_box = pygame.Rect(width / 2.5 - height_text.get_width() / 2 + 110, height / 1.85, mi.get_width() + 10, 25)

                    screen.fill(WHITE, height_box)
                    screen.fill(WHITE, width_box)
                    screen.fill(WHITE, mines_box)
                    
                    screen.blit(hei, (width / 2.5 - height_text.get_width() / 2 + 115, height / 3.15))
                    screen.blit(wid, (width / 2.5 - height_text.get_width() / 2 + 115, height / 2.45))
                    screen.blit(mi, (width / 2.5 - height_text.get_width() / 2 + 115, height / 1.98))

                    if h_C:
                        pygame.draw.rect(screen, (220, 20, 60), height_box, 3)
                    elif w_C:
                        pygame.draw.rect(screen, (220, 20, 60), width_box, 3)
                    if m_C:
                        pygame.draw.rect(screen, (220, 20, 60), mines_box, 3)

            pygame.display.update()




    else:
        
        screen = pygame.display.set_mode((cell_size*WIDTH +240, cell_size*HEIGHT +40))

        # Reset button
        resetButton = pygame.Rect(
            (cell_size*WIDTH +240) - ((600 / 3) - BOARD_PADDING * 2 +10), (1 / 3) * (cell_size*HEIGHT +40) + 20,
            ((360 +240) / 3) - BOARD_PADDING * 2, 50
        )
        buttonText = mediumFont.render("Reset", True, BLACK)
        buttonRect = buttonText.get_rect()
        buttonRect.center = resetButton.center
        pygame.draw.rect(screen, WHITE, resetButton)
        screen.blit(buttonText, buttonRect)

        # Display text
        text = "Lost" if lost else "Won" if game.mines == flags else ""
        colour = (220, 20, 60) if lost else (127,255,0)
        text = mediumFont.render(text, True, colour)
        textRect = text.get_rect()
        textRect.center = ((5 / 6) * (cell_size*WIDTH +240), (2 / 3) * (cell_size*HEIGHT +40))
        screen.blit(text, textRect)

        # Play game mode
        if not beta_mode:
            move = None

            # AI Move button
            aiButton = pygame.Rect(
                (cell_size*WIDTH +240) - ((600 / 3) - BOARD_PADDING * 2 +10), (1 / 3) * (cell_size*HEIGHT +40) - 50,
                (600 / 3) - BOARD_PADDING * 2, 50
            )
            buttonText = mediumFont.render("AI Move", True, BLACK)
            buttonRect = buttonText.get_rect()
            buttonRect.center = aiButton.center
            pygame.draw.rect(screen, WHITE, aiButton)
            screen.blit(buttonText, buttonRect)

            # Draw board
            cells = []
            for i in range(HEIGHT):
                row = []
                for j in range(WIDTH):

                    # Draw rectangle for cell
                    rect = pygame.Rect(
                        board_origin[0] + j * cell_size,
                        board_origin[1] + i * cell_size,
                        cell_size, cell_size
                    )
                    
                    pygame.draw.rect(screen, GRAY, rect)    
                    pygame.draw.rect(screen, WHITE, rect, 3)

                    # Add a mine, flag, or number if needed
                    if game.is_mine((i, j)) and lost:
                        screen.blit(mine, rect)
                    elif (i, j) in flags:
                        screen.blit(flag, rect)
                    elif (i, j) in revealed:
                        neighbors = smallFont.render(
                            str(game.nearby_mines((i, j))),
                            True, BLACK
                        )
                        neighborsTextRect = neighbors.get_rect()
                        neighborsTextRect.center = rect.center
                        screen.blit(neighbors, neighborsTextRect)

                    row.append(rect)
                cells.append(row)

            left, _, right = pygame.mouse.get_pressed()

            # Check for a right-click to toggle flagging
            if right == 1 and not lost:
                mouse = pygame.mouse.get_pos()
                for i in range(HEIGHT):
                    for j in range(WIDTH):
                        if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                            if (i, j) in flags:
                                flags.remove((i, j))
                            else:
                                flags.add((i, j))
                            time.sleep(0.2)

            elif left == 1:
                mouse = pygame.mouse.get_pos()

                # If AI button clicked, make an AI move
                if aiButton.collidepoint(mouse) and not lost:
                    move = ai.make_safe_move()
                    if move is None:
                        move = ai.make_random_move()
                        if move is None:
                            flags = ai.mines.copy()
                            print("No moves left to make.")
                        else:
                            print("No known safe moves, AI making random move.")
                    else:
                        print("AI making safe move.")
                    time.sleep(0.2)

                # Reset game state
                elif resetButton.collidepoint(mouse):
                    game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                    ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
                    revealed = set()
                    flags = set()
                    lost = False
                    continue

                # User-made move
                elif not lost:
                    for i in range(HEIGHT):
                        for j in range(WIDTH):
                            if (cells[i][j].collidepoint(mouse)
                                    and (i, j) not in flags
                                    and (i, j) not in revealed):
                                move = (i, j)

            # Make move and update AI knowledge
            if move:
                if game.is_mine(move):
                    lost = True
                else:
                    nearby = game.nearby_mines(move)
                    revealed.add(move)
                    ai.add_knowledge(move, nearby)
        
        # Solve game mode
        else:
            store = dict()
            rr = True
            while rr:
                # Draw board
                cells = []
                for i in range(HEIGHT):
                    row = []
                    for j in range(WIDTH):

                        # Draw rectangle for cell
                        rect = pygame.Rect(
                            board_origin[0] + j * cell_size,
                            board_origin[1] + i * cell_size,
                            cell_size, cell_size
                        )
                        if (i,j) not in revealed and (i,j) in ai.safes:
                            pygame.draw.rect(screen, (152,251,152), rect)
                        elif (i,j) not in revealed and (i,j) in ai.mines:
                            pygame.draw.rect(screen, (240,128,128), rect)
                        else:
                            pygame.draw.rect(screen, GRAY, rect)
                        if (i, j) == selected:
                            pygame.draw.rect(screen, (220, 20, 60), rect, 3)

                            # Added probability system to make a guess
                            if (i, j) not in revealed:
                                prob = 0
                                for l in ai.knowledge:
                                    if (i, j) in l.cells:
                                        if prob > 0:
                                            prob += prob*l.count/len(l.cells)
                                        else:
                                            prob = l.count/len(l.cells)

                                if prob == 0:
                                    prob = MINES / ((HEIGHT*WIDTH) - len(ai.safes))
                                if (i, j) in ai.mines:
                                    prob = 1
                                if (i, j) in ai.safes:
                                    prob = 0

                                text = "{:.1f}%".format(prob*100)
                                percentText = pygame.font.Font(OPEN_SANS, 15).render(text, True, (210, 43, 43))
                                percentRect = percentText.get_rect()
                                percentRect.center = rect.center
                                
                                screen.blit(percentText, percentRect)

                        else:
                            pygame.draw.rect(screen, WHITE, rect, 3)

                        # Add a mine, flag, or number if needed
                        if game.is_mine((i, j)) and lost:
                            screen.blit(mine, rect)
                        elif (i, j) in flags:
                            screen.blit(flag, rect)
                        elif (i, j) in revealed:
                            neighbors = smallFont.render(
                                str(store[(i, j)]),
                                True, BLACK
                            )
                            neighborsTextRect = neighbors.get_rect()
                            neighborsTextRect.center = rect.center
                            screen.blit(neighbors, neighborsTextRect)

                        row.append(rect)
                    cells.append(row)

                for eve in pygame.event.get():
                    # Added select cell concept
                    if eve.type == pygame.QUIT:
                        sys.exit()
                    elif eve.type == pygame.KEYDOWN:
                        if eve.key == pygame.K_ESCAPE:
                            instructions = True
                            rr = False
                        if selected:
                            try:
                                if int(eve.unicode) in range(0, 10):
                                    nearby = int(eve.unicode)
                                    revealed.add(selected)

                                    if selected in store.keys():
                                        ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
                                        store.pop(selected)
                                        for ss in store.keys():
                                            ai.add_knowledge(ss, store[ss])
                                        ai.add_knowledge(selected, nearby)
                                        store[selected] = nearby
                                    else:    
                                        ai.add_knowledge(selected, nearby)
                                        store[selected] = nearby
                                    
                            except:
                                pass # Reject any unintended input

                    if eve.type == pygame.MOUSEBUTTONDOWN:
                        cc = False
                        mouse = pygame.mouse.get_pos()
                        for i in range(HEIGHT):
                            for j in range(WIDTH):
                                if cells[i][j].collidepoint(mouse):
                                    selected = (i, j)
                                    cc = True
                        if not cc:
                            selected = ()
                        
                        mouse = pygame.mouse.get_pos()

                        # Reset game state
                        if resetButton.collidepoint(mouse):
                            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                            ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
                            revealed = set()
                            flags = set()
                            lost = False
                            continue
                                    
                pygame.display.flip()
    pygame.display.flip()
