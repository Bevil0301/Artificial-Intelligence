from functools import lru_cache

import pygame
from choice_menu import ChoiceMenu
import puzzle
import vacuum
from graphics import INK, MUTED, TEAL, WHITE, backdrop, box, card, heading, native_display
from search import ALGORITHMS, Problem


def play():
    screen = native_display()
    pygame.display.set_caption("Search Lab")
    games = (puzzle, vacuum)
    game = games[0]
    algorithm = next(iter(ALGORITHMS))
    starts = {g: g.START for g in games}
    game_switch = pygame.Rect(30,588,402,48)
    algorithm_switch = pygame.Rect(448,588,402,48)
    menu = None
    regular = pygame.font.match_font("segoeui,arial,dejavusans")
    bold = pygame.font.match_font("segoeui,arial,dejavusans", bold=True)

    @lru_cache(maxsize=300)
    def glyph(value, size, color, strong):
        font = fonts.setdefault((size, strong), None)
        if font is None:
            font = fonts[size, strong] = pygame.font.Font(bold if strong else regular, size)
        return font.render(str(value), True, color)

    def label(value, x, y, size=18, color=INK, strong=False, center=False):
        image = glyph(value, size, color, strong)
        screen.blit(image, image.get_rect(center=(x,y)) if center else (x,y))

    fonts = {}
    def solve(initial):
        problem = Problem(initial, game.is_goal, game.actions, game.result)
        trace = []
        path = ALGORITHMS[algorithm](problem, trace)
        moves = [next(a for a in game.actions(s) if game.result(s,a)==n) for s,n in zip(path,path[1:])]
        visited = [node for node,_,_ in trace if node is not None]
        return trace, path, moves, visited

    initial = starts[game]
    trace,path,moves,visited = solve(initial)
    buttons = [pygame.Rect(x,527,w,44) for x,w in [(30,120),(160,98),(268,115),(393,220),(623,227)]]
    clock = pygame.time.Clock()
    speed = index = 0
    phase = 0.0
    playing, review = True, False
    speeds = (1,2,4,8)
    while True:
        dt = clock.tick(120) / 1000
        total = len(trace) if review else len(path)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if menu is not None:
                closed, choice = menu.event(event)
                if closed:
                    if choice is not None and choice != menu.current:
                        if menu.anchor == game_switch:
                            game = next(g for g in games if g.TITLE == choice)
                        else:
                            algorithm = choice
                        initial = starts[game]
                        trace,path,moves,visited = solve(initial)
                        index,phase,playing,review = 0,0.0,True,False
                    menu = None
                    pygame.key.stop_text_input()
                    clock.tick()
                    dt = 0
                continue
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_switch.collidepoint(event.pos):
                    menu = ChoiceMenu(game_switch, [g.TITLE for g in games], game.TITLE, False)
                    continue
                if algorithm_switch.collidepoint(event.pos):
                    menu = ChoiceMenu(algorithm_switch, ALGORITHMS, algorithm, True)
                    pygame.key.start_text_input()
                    continue
                for k,rect in enumerate(buttons):
                    if rect.collidepoint(event.pos):
                        if k == 4:
                            draft = game.edit_start(screen,label,initial)
                            if draft is not None:
                                initial = starts[game] = draft
                                trace,path,moves,visited = solve(initial)
                                index,phase,playing,review = 0,0.0,True,False
                            clock.tick()
                        elif k == 0 and index < total-1:
                            playing = not playing
                        elif k == 2:
                            speed = (speed+1) % len(speeds)
                        else:
                            if k == 3:
                                review = not review
                            index,phase,playing = 0,0.0,True
                        dt = 0
        total = len(trace) if review else len(path)
        if playing and menu is None:
            phase += min(dt,0.15)*speeds[speed]/1.15
            index = min(total-1,index+int(phase))
            phase %= 1
            if index == total-1:
                phase,playing = 0.0,False
        t = phase*phase*(3-2*phase)
        screen.blit(backdrop(),(0,0))
        heading(screen,label,f"{algorithm} · {game.TITLE}","Quá trình duyệt" if review else "Đường đi lời giải")
        label(f"{'Vòng' if review else 'Bước'}  {index} / {total-1}",650,44,20,TEAL,True)
        if review:
            current, pending, pending_count = trace[index]
            for col,(name,states) in enumerate([("Node",[current] if current else []),("Frontier",pending),("Explored",visited[:min(index,6)])]):
                x = 30+col*278
                card(screen,(x,108,264,374),"#1c3041","#435a6b")
                box(screen,(x+16,157,232,3),[TEAL,"#ffc477","#87b9ff"][col],1)
                label(name,x+16,123,22,INK,True)
                count = pending_count if name == "Frontier" else index if name == "Explored" else len(states)
                label(str(count),x+210,127,18,TEAL)
                for j,state in enumerate(states[:6]):
                    game.draw_state(screen,label,state,state,0,x+14+(j%2)*124,174+(j//2)*91,80)
                if not states:
                    label("Rỗng",x+16,180,17,MUTED)
                if count>6:
                    label(f"+ {count-6} trạng thái",x+16,450,16,MUTED)
        else:
            card(screen,(30,108,480,374),"#203548","#506779")
            card(screen,(526,108,324,374),"#192b3c","#3c5369")
            pygame.draw.line(screen,"#364d60",(549,370),(827,370))
            label("Bàn chơi",50,124,19,MUTED,True)
            state = path[index]
            game.draw_state(screen,label,state,path[min(index+1,total-1)],t,122,game.BOARD_Y,294)
            label("Trạng thái đích",550,126,21,INK,True)
            game.draw_state(screen,label,game.GOAL,game.GOAL,0,607,game.GOAL_Y,162)
            label("Hành động",550,387,16,MUTED)
            move = moves[index] if index<len(moves) else "Đã tới đích"
            label({"suck":"Hút bụi","left":"Sang trái","right":"Sang phải"}.get(move,move),550,411,25,TEAL,True)
        box(screen,(30,502,820,6),"#30485b",3)
        progress = round(820*(index+phase)/max(1,total-1))
        if progress:
            box(screen,(30,502,progress,6),TEAL,3)
        captions = ["Tạm dừng" if playing else ("Phát lại" if index==total-1 else "Tiếp tục"),"Từ đầu",f"Tốc độ ×{speeds[speed]}","Xem lời giải" if review else "Xem quá trình duyệt","Chỉnh trạng thái đầu"]
        for k,(rect,caption) in enumerate(zip(buttons,captions)):
            hover = rect.collidepoint(pygame.mouse.get_pos())
            fill = ("#cefff3" if hover else TEAL) if k==0 else ("#3a5268" if hover else "#263c50")
            box(screen,rect,fill,9)
            label(caption,*rect.center,18,"#142839" if k==0 else INK,True,True)
        for rect, caption in [(game_switch, f"Bài toán: {game.TITLE}"), (algorithm_switch, f"Thuật toán: {algorithm}")]:
            hovered = rect.collidepoint(pygame.mouse.get_pos())
            active = menu is not None and menu.anchor == rect
            pygame.draw.rect(screen, "#30495e" if hovered or active else "#203447", rect, border_radius=8)
            pygame.draw.rect(screen, TEAL if active else "#678294", rect, width=1, border_radius=8)
            text_area = rect.inflate(-32,0)
            text_area.width -= 24
            screen.set_clip(text_area)
            image = glyph(caption,18,INK,True)
            screen.blit(image,image.get_rect(midleft=(text_area.left,rect.centery)))
            screen.set_clip(None)
            x,y = rect.right-23,rect.centery
            direction = -1 if active else 1
            pygame.draw.polygon(screen,TEAL,[(x-5,y-2*direction),(x+5,y-2*direction),(x,y+4*direction)])
        if menu is not None:
            menu.draw(screen,label)
        pygame.display.flip()


if __name__ == "__main__":
    play()
