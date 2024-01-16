import os
import sys
import math
import random
import pygame as pg
from pygame.sprite import AbstractGroup
import time

WIDTH = 1600
HEIGHT = 900
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
ROUND_NOW = 0  # 今何ラウンド目か

class Card(pg.sprite.Sprite):
    '''
    カードに関するクラス
    '''
    card = {
        "h":
            {
                "A": 'h01@2x.png',
                "2": 'h02@2x.png',
                "3": 'h03@2x.png',
                "4": 'h04@2x.png',
                "5": 'h05@2x.png',
                "6": 'h06@2x.png',
                "7": 'h07@2x.png',
                "8": 'h08@2x.png',
                "9": 'h09@2x.png',
                "10": 'h10@2x.png',
                "J": 'h11@2x.png',
                "Q": 'h12@2x.png',
                "K": 'h13@2x.png'
            },
        "s":
            {
                "A": 's01@2x.png',
                "2": 's02@2x.png',
                "3": 's03@2x.png',
                "4": 's04@2x.png',
                "5": 's05@2x.png',
                "6": 's06@2x.png',
                "7": 's07@2x.png',
                "8": 's08@2x.png',
                "9": 's09@2x.png',
                "10": 's10@2x.png',
                "J": 's11@2x.png',
                "Q": 's12@2x.png',
                "K": 's13@2x.png'
            },
        "d":
            {
                "A": 'd01@2x.png',
                "2": 'd02@2x.png',
                "3": 'd03@2x.png',
                "4": 'd04@2x.png',
                "5": 'd05@2x.png',
                "6": 'd06@2x.png',
                "7": 'd07@2x.png',
                "8": 'd08@2x.png',
                "9": 'd09@2x.png',
                "10": 'd10@2x.png',
                "J": 'd11@2x.png',
                "Q": 'd12@2x.png',
                "K": 'd13@2x.png'
            },
        "k":
            {
                "A": 'k01@2x.png',
                "2": 'k02@2x.png',
                "3": 'k03@2x.png',
                "4": 'k04@2x.png',
                "5": 'k05@2x.png',
                "6": 'k06@2x.png',
                "7": 'k07@2x.png',
                "8": 'k08@2x.png',
                "9": 'k09@2x.png',
                "10": 'k10@2x.png',
                "J": 'k11@2x.png',
                "Q": 'k12@2x.png',
                "K": 'k13@2x.png'
            },
        "None":
            {
                "None": "back@2x.png"
            }
        }
    suits = ['h', 's', 'd', 'k']

    ranks = ["A","2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    
    def __init__(self, s: str, r: str):
        '''
        カード画像のSurfaceを生成する
        引数1 s: カードの絵柄
        引数2 r: カードの数字
        '''
        self.r = r
        self.s = s
    
    def __int__(self) -> int:
        '''
        カードの数字を返す関数
        戻り値 num: カードの数字
        '''
        if self.r == 'J' or self.r == 'Q' or self.r == 'K':
            num = 10
        elif self.r == 'A':
            num = 1
        else:
            num = int(self.r)
        return num
    
    def __str__(self):
        return self.s


class Deck():
    '''
    カードをシャッフルし、山札とするクラス
    このクラスを利用することで重複をなくす
    '''
    def __init__(self):
        self.cards = []
        for i in Card.suits:
            for j in Card.ranks:
                self.cards.append(Card(i, j))
        random.shuffle(self.cards)

    def draw(self) -> Card:
        '''
        シャッフルされたカードのリストから要素を取り出す関数
        戻り値: Cardクラスのインスタンス
        '''
        if len(self.cards) == 0:
            return
        return self.cards.pop()


class Image(pg.sprite.Sprite):
    '''
    カードのSurfaceを作成するクラス
    '''
    def __init__(self, s: str, r: int, xy: tuple[int, int]):
        '''
        引数1: カードの絵柄
        引数2: カードの数字
        引数3: カードの座標
        '''
        super().__init__()
        self.s = s
        self.r = r
        self.image = pg.transform.rotozoom(pg.image.load(f'{MAIN_DIR}/playingcard-mini/{Card.card[s][r]}'), 0, 1.5)
        self.rect = self.image.get_rect()
        self.rect.center = xy
        
    def update(self, screen: pg.Surface):
        screen.blit(self.image, self.rect)


class Player():
    '''
    プレイヤーのトータルを保存し、バースト判定を行うクラス
    '''
    def __init__(self):
        self.total = 0  # カードの合計値
        self.bj = False  # ブラックジャックかどうか判定するフラッグ
        
    def match(self):
        '''
        トータルからバーストしていないか確認する関数
        '''
        if self.total == 21:
            self.bj = True
            return True
        
        elif self.total < 21:
            return True
        
        else:
            return False

    
class Chip():
    """
    チップに関するクラス
    """
    def __init__(self, c: int):
        self.value = c      # 手持ちのチップの数
        self.bet = 0        # ベットするチップの数
        self.now_bet = 0    # ベットされたチップの数
        self.bet_flag = 0   # ベットしたかどうか
        self.font = pg.font.Font(None, 100)
        self.color = (128, 0, 0)
        self.image_v = self.font.render(f"Chip: {self.value}", 0, self.color)
        self.rect_v = self.image_v.get_rect()
        self.rect_v.center = 180, HEIGHT-50
        self.image_b = self.font.render(f"Bet?: {self.bet}", 0, self.color)
        self.rect_b = self.image_b.get_rect()
        self.rect_b.center = 130, 50
        self.image_nb = self.font.render(f"Bet: {self.now_bet}", 0, self.color)
        self.rect_nb = self.image_nb.get_rect()
        self.rect_nb.center = 110, 50

    def update(self, screen: pg.Surface):
        self.image_v = self.font.render(f"Chip: {self.value}", 0, self.color)
        screen.blit(self.image_v, self.rect_v)

        if self.bet_flag == 0:
            self.image_b = self.font.render(f"Bet?: {self.bet}", 0, self.color)
            screen.blit(self.image_b, self.rect_b)
            
                
        else:
            self.image_nb = self.font.render(f"Bet: {self.now_bet}", 0, self.color)
            screen.blit(self.image_nb, self.rect_nb)




class Game(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.deck = Deck()
        self.p = Player()
        self.d = Player()
        
        self.pc = [self.deck.draw() for _ in range(2)]
        self.dc = [self.deck.draw()]
        self.dc.append(Card('None', 'None'))
        
        self.p_cards = pg.sprite.Group()
        self.d_cards = pg.sprite.Group()
        
        self.p.total += int(self.pc[0]) + int(self.pc[1])
        self.d.total += int(self.dc[0])
        
        
    #def add_group(self):
        
    def dc_draw(self):
        dc2 = self.deck.draw()
        self.dc.append(dc2)
        self.d.total += int(dc2)
        

'''
class Button(pg.sprite.Sprite):
    def __init__(self, text, b_color: tuple[int, int, int], hw: tuple[int, int], xy: tuple[int, int]):
        super().__init__()
        
        self.text = text
        self.font = pg.font.Font(None, 50)
        
        self.b_color = b_color
        self.sf = pg.Surface(hw)
        self.xy = xy
        self.hw = hw
        
        self.button = pg.draw.rect(self.sf, self.b_color, self.hw)
        self.rect = self.sf.get_rect()
        self.f_color = (0, 0, 0)
        self.tx = self.font.render(self.text, 0, self.f_color)
        
        self.rect.center = self.xy
    def update(self):
        self.tx = self.font.render(self.text, 0, self.color)
        self.sf.blit(self.tx, self.rect)
'''

def draw_text(screen, text, size, x, y, color=(255,255,255), font_path=None):
    font = pg.font.Font(font_path, size) if font_path else pg.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

class Hit(pg.sprite.Sprite):
    """
    ヒットに関するクラス
    """
    def __init__(self, card: Card, hit_num):
        """
        新たにトランプを一枚引く
        引数1 card：持ち札のカード
        引数2 hit_num：ヒットした回数
        """
        super().__init__()
        gara = ["h", "s", "d", "k"]
        num = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        # self.img = pg.transform.rotozoom(pg.image.load(f'{MAIN_DIR}/playingcard-mini/{Card.card[random.choice(gara)][random.choice(num)]}'), 0, 1.5)
        self.img = Deck.draw()
        self.rct = self.img.get_rect()
        self.rct.centerx = 850 + 100*hit_num
        self.rct.centery = 900-225

    def update(self, screen: pg.Surface):
        screen.blit(self.img, self.rct)


class Stand(pg.sprite.Sprite):
    """
    スタンドに関するクラス
    """
    def __init__(self, life: int):
        # スタンドと表示する
        super().__init__()
        self.font = pg.font.Font(None, 50)
        self.color = (255, 0, 0)
        self.image = self.font.render(f"Stand", 0, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH/2, HEIGHT/2
        self.life = life

    def update(self, screen: pg.Surface):
        self.image = self.font.render(f"Stand", 0, self.color)
        screen.blit(self.image, self.rect)
        self.life -= 1
        if self.life < 0:
            self.kill()


class Round:
    """
    ラウンド数に関するクラス
    """
    def __init__(self, round_max: int):
        """
        ラウンド数を数えたい
        引数 round_max: ゲームを何回行うか
        """
        self.round_max = round_max

    def update(self, screen:pg.Surface):
        """
        ラウンド数を更新したい
        """
        font = pg.font.SysFont(None, 100)
        text = font.render("round "+str(ROUND_NOW)+"/"+str(self.round_max), True, (0, 255, 255))
        screen.blit(text, [1200, 0])
        

def main():
    global ROUND_NOW
    pg.display.set_caption('black jack')
    screen = pg.display.set_mode((WIDTH, HEIGHT))  
    chip = Chip(200)
    screen.fill((70, 128, 79))
    pg.mouse.set_visible(True)  # マウスカーソル表示

    
    player_cards = pg.sprite.Group()  # プレイヤーのカードを保存するスプリットグループ
    dealer_cards = pg.sprite.Group()  # ディーラーのカードを保存するスプリットグループ
    #buttons = pg.sprite.Group()
    hit = pg.sprite.Group()
    stand = pg.sprite.Group()
    
    p = Player()
    d = Player()
    
    deck = Deck()
    pc = [deck.draw() for _ in range(2)]
    dc = [deck.draw()]
    dc.append(Card("None", "None"))
    #p1 = deck.draw() 
    #p2 = deck.draw()
    #d1 = deck.draw()
    #d2 = Card("None", "None") # 裏の画像を指定
    p.total += int(pc[0]) + int(pc[1])
    d.total += int(dc[0])
    #p.total += int(p1) + int(p2)
    
    
    round_max = 1  # 何ラウンドゲームを行うか
    round_flag = 1  # ラウンド数設定画面か否か
    card = Card("d",'A')
    clock = pg.time.Clock()
    
    hit_num = 0  # プレイヤーがそのラウンドでヒットした回数
    while round_flag:  # ラウンド数設定
        screen.fill((70, 128, 79))
        key_lst = pg.key.get_pressed()
        
        font = pg.font.SysFont(None, 50)
        text1 = font.render("Set the number of rounds using the arrow keys.", True, (0, 255, 255))
        text2 = font.render("Confirm with enter key.", True, (0, 255, 255))
        screen.blit(text1, [0, 0])
        screen.blit(text2, [0, 50])

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:  # 上キーで増やす
                round_max += 1
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:  # 下キーで減らす
                if round_max > 1:
                    round_max -= 1
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:  # リターンキーで決定
                round_flag = 0
        round = Round(round_max)
        round.update(screen)
        pg.display.update()

    tmr = 0
    z = 0
    b = 0
    clock = pg.time.Clock()
    hit_num = 0  # プレイヤーがそのラウンドでヒットした回数


    while True:
            
        #key_lst = pg.key.get_pressed()
        for i in range(2):
            player_cards.add(Image(str(pc[i]), pc[i].r, (750+100*(i+1), 900-225)))
            dealer_cards.add(Image(str(dc[i]), dc[i].r, (750+100*(i+1), 225)))
        #player_cards.add(Image(str(p1), p1.r, (750, 900-225)))
        #player_cards.add(Image(str(p2), p2.r, (850, 900-225)))
        #dealer_cards.add(Image(str(d1), d1.r, (750, 225)))
        #dealer_cards.add(Image(str(d2), d2.r, (850, 225)))

        round = Round(round_max)

        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                return

            if chip.bet_flag == 0:
                screen.fill((70, 128, 79))
                if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                    if chip.bet < chip.value :
                        chip.bet += 1
                if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                    if chip.bet > 0:
                        chip.bet -= 1
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    chip.bet_flag = 1
                    chip.now_bet = chip.bet
                    chip.value -= chip.bet
                    chip.bet = 0
                    
            if chip.bet_flag == 1:
                Flag_game = True
                draw_text(screen, "HIT(h) or STAND(s)", 100, 50, 700)
                if Flag_game == True:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_h:
                            a = deck.draw()
                            player_cards.add(Image(str(a), a.r, (1050+b, 900-225)))
                            p.total += int(a)
                            b += 100
                            if p.total > 21:
                                dc[1] = deck.draw()
                                d.total = int(dc[0]) + int(dc[1])
                                dealer_cards.add(Image(str(dc[1]), dc[1].r, (950+z, 225)))
                                player_cards.update(screen)
                                dealer_cards.update(screen)
                                pg.display.update()
                                Flag_game = False
                                #break

                        elif event.key == pg.K_s:
                            dc[1] = deck.draw()  # 裏の画像を普通のトランプにかきかえ
                            d.total += int(dc[1])
                            dealer_cards.add(Image(str(dc[1]), dc[1].r, (950+z, 225)))
                            dealer_cards.update(screen)
                            pg.display.update()
                            if d.total >= 17:
                                Flag_game = False
                            else:
                                while True:
                                    z += 100
                                    x = deck.draw()
                                    dealer_cards.add(Image(str(x), x.r, (950+z, 225)))
                                    d.total += int(x)
                                    dealer_cards.update(screen)
                                    pg.display.update()
                                    if d.total >= 18:
                                        Flag_game = False
                                        break
                                    
                if Flag_game == False:
                    if p.total > 21:
                        draw_text(screen, "YOU LOSE", 100, 100, 550)
                        chip.now_bet = 0
                        pg.display.update()
                        player_cards.draw(screen)
                        player_cards.update(screen)
                        dealer_cards.draw(screen)
                        dealer_cards.update(screen)
                        chip.update(screen)
                        hit.update(screen)
                        stand.update(screen)
                        round.update(screen)
                        time.sleep(2)
                        chip.bet_flag = 0
                        #return
                    
                    elif p.total <= 21 and d.total <= 21:
                        if p.total < d.total:
                            draw_text(screen, "YOU LOSE", 100, 100, 550)
                            chip.now_bet *= 2
                            pg.display.update()
                            player_cards.draw(screen)
                            player_cards.update(screen)
                            dealer_cards.draw(screen)
                            dealer_cards.update(screen)
                            chip.update(screen)
                            hit.update(screen)
                            stand.update(screen)
                            round.update(screen)
                            time.sleep(2)
                            chip.bet_flag = 0
                            #return
                        elif p.total > d.total:
                            draw_text(screen, "YOU WIN", 100, 100, 550)
                            chip.now_bet *= 2
                            chip.value += chip.now_bet
                            pg.display.update()
                            player_cards.draw(screen)
                            player_cards.update(screen)
                            dealer_cards.draw(screen)
                            dealer_cards.update(screen)
                            chip.update(screen)
                            hit.update(screen)
                            stand.update(screen)
                            round.update(screen)
                            time.sleep(2)
                            chip.bet_flag = 0
                            #return
                        
                    elif d.total > 21 and p.total <= 21: 
                        draw_text(screen, "YOU WIN", 100, 100, 550)
                        chip.now_bet *= 2
                        chip.value += chip.now_bet
                        pg.display.update()
                        player_cards.draw(screen)
                        player_cards.update(screen)
                        dealer_cards.draw(screen)
                        dealer_cards.update(screen)
                        chip.update(screen)
                        hit.update(screen)
                        stand.update(screen)
                        round.update(screen)
                        time.sleep(2)
                        chip.bet_flag = 0
                        #return
                        
                    p = Player()
                    d = Player()
    
                    deck = Deck()
                    pc = [deck.draw() for _ in range(2)]
                    dc = [deck.draw()]
                    dc.append(Card("None", "None"))
                    p.total += int(pc[0]) + int(pc[1])
                    d.total = int(dc[0])
                    player_cards = pg.sprite.Group()  # プレイヤーのカードを保存するスプリットグループ
                    dealer_cards = pg.sprite.Group() 
                    b = 0
                    z = 0
                    
                    ROUND_NOW += 1
                    if ROUND_NOW == round_max:
                        draw_text(screen, "END GAME", 100, 600, 400, (255, 0, 0))
                        pg.display.update()
                        round.update(screen)
                        player_cards.draw(screen)
                        player_cards.update(screen)
                        dealer_cards.draw(screen)
                        dealer_cards.update(screen)
                        chip.update(screen)
                        hit.update(screen)
                        stand.update(screen)
                        time.sleep(2)
                        return
                '''    
                # s押下でスタンド
                if event.type == pg.KEYDOWN and event.key == pg.K_s:
                    hit_num = 0  # ヒット回数のリセット
                    stand.add(Stand(60))
                
                # h押下でヒット
                if event.type == pg.KEYDOWN and event.key == pg.K_h:
                    hit_num += 1
                    p3 = deck.draw()
                    p.total += int(p3)
                    player_cards.add(Image(str(p3), p3.r, (850+hit_num*100, 900-225)))
                    print(p.total)
                    if p.match() == False:
                        pg.display.update()
                        time.sleep(2)
                        return
               '''
        if tmr % 10 == 0:
            print(str(pc[0]),pc[0].r, 'P_total:', p.total, 'D_total:', d.total, 'flag:', p.total > d.total)
            print()
            
        player_cards.draw(screen)
        player_cards.update(screen)
        dealer_cards.draw(screen)
        dealer_cards.update(screen)
        chip.update(screen)
        hit.update(screen)
        stand.update(screen)
        round.update(screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
