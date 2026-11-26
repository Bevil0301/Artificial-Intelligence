import pygame
from graphics import INK, MUTED, TEAL, box


class ChoiceMenu:
    row_height = 34
    visible_rows = 6

    def __init__(self, anchor, choices, current, searchable):
        self.anchor = anchor
        self.choices = list(choices)
        self.current = current
        self.searchable = searchable
        self.query = ""
        self.filter()
        self.focus = self.options.index(current)
        self.offset = max(0, self.focus - self.visible_rows + 1)

    def filter(self):
        self.options = [name for name in self.choices if self.query.casefold() in name.casefold()]
        self.focus = self.offset = 0

    def bounds(self):
        header = 44 if self.searchable else 0
        rows = max(1, min(len(self.options), self.visible_rows))
        height = header + rows * self.row_height + 12
        frame = pygame.Rect(self.anchor.x, self.anchor.top - height - 6, self.anchor.w, height)
        return frame, frame.y + header + 6

    def event(self, event):
        frame, top = self.bounds()
        if event.type == pygame.TEXTINPUT and self.searchable:
            self.query += event.text
            self.filter()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True, None
            if event.key == pygame.K_BACKSPACE:
                self.query = self.query[:-1]
                self.filter()
            if self.options:
                if event.key == pygame.K_RETURN:
                    return True, self.options[self.focus]
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    self.focus = max(0,min(len(self.options)-1,self.focus + (1 if event.key==pygame.K_DOWN else -1)))
                    self.offset = max(self.focus-self.visible_rows+1,min(self.offset,self.focus))
        elif event.type == pygame.MOUSEWHEEL:
            self.offset = max(0,min(max(0,len(self.options)-self.visible_rows),self.offset-event.y))
            self.focus = max(self.offset,min(self.focus,self.offset+self.visible_rows-1))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not frame.collidepoint(event.pos):
                return True, None
            row = (event.pos[1]-top)//self.row_height
            idx = self.offset + row
            if 0 <= row < self.visible_rows and idx < len(self.options):
                return True, self.options[idx]
        return False, None

    def draw(self, screen, label):
        frame, top = self.bounds()
        box(screen,frame,"#6a8798",10)
        box(screen,frame.inflate(-2,-2),"#182c3d",9)
        clip = screen.get_clip()
        screen.set_clip(frame.inflate(-12,-6))
        if self.searchable:
            label(self.query or "Gõ để lọc thuật toán…",frame.x+15,frame.y+10,17,INK if self.query else MUTED)
            pygame.draw.line(screen,"#496072",(frame.x+12,top-4),(frame.right-12,top-4))
        if not self.options:
            label("Không tìm thấy thuật toán",frame.x+15,top+4,16,MUTED)
        for row,name in enumerate(self.options[self.offset:self.offset+self.visible_rows]):
            rect = pygame.Rect(frame.x+6,top+row*self.row_height,frame.w-16,self.row_height)
            if rect.collidepoint(pygame.mouse.get_pos()) or self.offset+row == self.focus:
                box(screen,rect,"#304d60",5)
            if name == self.current:
                box(screen,(rect.x+2,rect.y+8,3,18),TEAL,1)
            label(name,rect.x+11,rect.y+4,17,INK)
        if len(self.options)>self.visible_rows:
            h = self.visible_rows*self.row_height
            thumb = max(12,h*self.visible_rows//len(self.options))
            y = top+(h-thumb)*self.offset//(len(self.options)-self.visible_rows)
            box(screen,(frame.right-8,y,3,thumb),TEAL,1)
        screen.set_clip(clip)
