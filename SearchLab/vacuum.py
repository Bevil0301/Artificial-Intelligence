import pygame
from graphics import INK, MUTED, TEAL, WHITE, backdrop, box, card, heading

rooms = ("A", "B")
START = ("A", "D", "D")
GOAL = ("B", "C", "C")
TITLE = "Robot hút bụi"
BOARD_Y, GOAL_Y = (218, 219)


def is_goal(state):
    if state == GOAL:
        return True
    else:
        return False


def actions(state):
    i = rooms.index(state[0])
    valid = []
    if state[i + 1] == "D":
        valid.append("suck")
    if i > 0:
        valid.append("left")
    if i < len(rooms) - 1:
        valid.append("right")
    return valid


def result(state, action):
    i = rooms.index(state[0])
    new_state = list(state)
    if action == "suck":
        new_state[i + 1] = "C"
    elif action == "left":
        new_state[0] = rooms[i - 1]
    elif action == "right":
        new_state[0] = rooms[i + 1]
    return tuple(new_state)


def draw_state(screen,label,state,following,t,x,y,width):
    half = width//2
    height = half+14
    box(screen,(x,y,width,height),"#b8c9c1",max(5,width//25))
    for i,room in enumerate(rooms):
        left = x+i*half
        dirty = state[i+1]=="D"
        fade = 1-t if dirty and following[i+1]=="C" else 1
        clean = (211,235,218)
        base = tuple(round(c+(d-c)*fade) for c,d in zip(clean,(248,227,186))) if dirty else clean
        box(screen,(left+3,y+3,half-6,height-6),base,max(3,half//12))
        label(room,left+6,y+3,max(12,width//14),"#274353",True)
        if dirty:
            for dx,dy in [(0.75,0.48),(0.83,0.6),(0.68,0.67)]:
                radius = round(max(2,half//36)*fade)
                if radius:
                    pygame.draw.circle(screen,"#98703e",(round(left+half*dx),round(y+height*dy)),radius)
    start,end = rooms.index(state[0]),rooms.index(following[0])
    cx = round(x+half*(0.45+start+(end-start)*t))
    cy = y+height//2+4
    radius = max(7,half//5)
    for r,color in [(radius,"#0e2332"),(max(3,int(radius*0.86)),"#4b6b81"),(max(2,int(radius*0.65)),"#274355")]:
        box(screen,(cx-r,cy-r,2*r,2*r),color,r)
    pygame.draw.circle(screen,"#b4f6db",(cx+radius//4,cy-radius//3),max(2,radius//6))


def edit_start(screen, label, initial):
    draft = initial
    clock = pygame.time.Clock()
    controls = [(pygame.Rect(x, 520, w, 48), title) for x,w,title in
                [(32,160,"Mặc định"),(490,140,"Hủy"),(642,206,"Áp dụng và chạy")]]
    choices = [pygame.Rect(396,160+i*70,384,50) for i in range(3)]
    while True:
        clock.tick(60)
        screen.blit(backdrop(),(0,0))
        heading(screen,label,"Chỉnh trạng thái đầu","Bấm từng mục để đổi vị trí robot hoặc trạng thái phòng.")
        card(screen,(30,108,820,382),"#1b2d41","#3c5266")
        draw_state(screen,label,draft,draft,0,58,195,285)
        names = [f"Vị trí robot: phòng {draft[0]}"] + [
            f"Phòng {room}: " + ("Bẩn" if value == "D" else "Sạch")
            for room,value in zip(rooms,draft[1:])]
        for rect,name in zip(choices,names):
            card(screen,rect,"#263f54","#526a7b")
            label(name,*rect.center,19,INK,True,True)
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
                for i,rect in enumerate(choices):
                    if rect.collidepoint(event.pos):
                        values = list(draft)
                        if i == 0:
                            values[i] = "B" if values[i] == "A" else "A"
                        else:
                            values[i] = "C" if values[i] == "D" else "D"
                        draft = tuple(values)
