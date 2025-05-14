from pygame.image import load

class Card:

    card_img = load("sprites/Card.png")
    
    def __init__(self, content, x, y):
        self.content = content
        self.x = x
        self.y = y

    def Draw(self, canvas):
        canvas.blit(Card.card_img,(self.x,self.y))
        canvas.blit(self.content,(self.x,self.y))
