import pygame
from graphics import INK, MUTED, TEAL, WHITE, backdrop, box, card, heading

START = ((1, 2, 3), (4, 0, 6), (7, 5, 8))
GOAL = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
TITLE = "8-puzzle"
BOARD_Y, GOAL_Y = (169, 182)


def is_goal(state):
    if state == GOAL:
        return True
    else:
        return False


def actions(state):
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                break
        if state[r][c] == 0:
            break

    moves = []
    if r > 0:
        moves.append("Lên")
    if r < 2:
        moves.append("Xuống")
    if c > 0:
        moves.append("Trái")
    if c < 2:
        moves.append("Phải")
    return moves


def result(state, action):
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                break
        if state[r][c] == 0:
            break

    new_r, new_c = r, c
    if action == "Lên":
        new_r -= 1
    elif action == "Xuống":
        new_r += 1
    elif action == "Trái":
        new_c -= 1
    elif action == "Phải":
        new_c += 1

    board = [list(row) for row in state]
    board[r][c] = board[new_r][new_c]
    board[new_r][new_c] = 0
    return tuple(tuple(row) for row in board)


def draw_state(screen,label,state,following,t,x,y,width):
    box(screen,(x,y,width,width),"#101f30",max(5,width//20))
    pad = max(3,width//38)
    gap = max(2,width//52)
    tile = (width-2*pad-2*gap)//3
    inset = (width-3*tile-2*gap)//2
    targets = {n:(r,c) for r,row in enumerate(following) for c,n in enumerate(row)}
    for r,row in enumerate(state):
        for c,n in enumerate(row):
            if not n:
                continue
            nr,nc = targets[n]
            left = x+inset+round((c+(nc-c)*t)*(tile+gap))
            top = y+inset+round((r+(nr-r)*t)*(tile+gap))
            radius = max(3,tile//9)
            color = TEAL if (r,c)!=(nr,nc) else ("#d3e3f0" if n%2 else "#aec6da")
            box(screen,(left,top,tile,tile),"#647e92",radius)
            box(screen,(left,top,tile,max(2,tile-3)),color,radius)
            label(str(n),left+tile//2,top+tile//2,max(14,tile//2),"#172f41",True,True)


def edit_start(screen, label, initial):
    draft = initial
    clock = pygame.time.Clock()
    controls = [(pygame.Rect(x, 520, w, 48), title) for x,w,title in
                [(32,160,"Mặc định"),(490,140,"Hủy"),(642,206,"Áp dụng và chạy")]]
    area = pygame.Rect(275,130,330,330)
    while True:
        clock.tick(60)
        screen.blit(backdrop(),(0,0))
        heading(screen,label,"Chỉnh trạng thái đầu","Bấm một ô số cạnh ô trống để trượt ô đó. Có thể thực hiện nhiều lần.")
        card(screen,(30,108,820,382),"#1b2d41","#3c5266")
        draw_state(screen,label,draft,draft,0,area.x,area.y,area.width)
        for rect, caption in controls:
            primary = caption == "Áp dụng và chạy"
            box(screen,rect,TEAL if primary else "#32495b")
            label(caption,*rect.center,18,"#0b242e" if primary else INK,True,True)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                continue
            for rect,caption in controls:
                if rect.collidepoint(event.pos):
                    if caption == "Hủy":
                        return None
                    if caption == "Mặc định":
                        draft = START
                    else:
                        return draft
                    break
            else:
                if area.collidepoint(event.pos):
                    col = (event.pos[0]-area.x)//110
                    row = (event.pos[1]-area.y)//110
                    for action in actions(draft):
                        candidate = result(draft,action)
                        if candidate[row][col] == 0:
                            draft = candidate
                            break
