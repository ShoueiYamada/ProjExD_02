import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
    }


def check_bound(obj_rct: pg.Rect):

    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: # 横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: # 縦方向判定
        tate = False
    return yoko,tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    ####こうかとん####
    kk_img = pg.image.load("ex02/fig/3.png")
    

    
    #####爆弾####
    bomb = pg.Surface((10, 10))
    pg.draw.circle(bomb, (255, 0, 0), (10, 10), 10)
    bomb_rct = bomb.get_rect()
    x,y = random.randint(0,WIDTH),random.randint(0,HEIGHT) #ランダムな座標を設定する。
    bomb_rct.center = (x,y)#練習問題１
    vx, vy = +5, +5 #練習２　爆弾の移動
    
    
    """追加機能１"""
    kk_img_r =  pg.transform.flip(kk_img, True, False)
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    
    kouka_houkou ={
        (0,0) : pg.transform.rotozoom(kk_img, 0, 1.0),
        (-5,0) : pg.transform.rotozoom(kk_img, 0, 1.0),
        (-5,-5) : pg.transform.rotozoom(kk_img, 315, 1.0),
        (0,-5) : pg.transform.rotozoom(kk_img, 225, 1.0),
        (+5,-5) : pg.transform.rotozoom(kk_img_r, 45, 2.0),
        (+5,0) : pg.transform.flip(kk_img, True, False),
        (+5,+5) : pg.transform.rotozoom(kk_img_r, 315, 2.0),
        (0,+5) : pg.transform.rotozoom(kk_img, 90, 1.0),
        (-5,+5) : pg.transform.rotozoom(kk_img, 45, 1.0)
}
    kk_img = kouka_houkou[(0,0)]
    kk_rct = kk_img.get_rect()
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400)  
    
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        
        if kk_rct.colliderect(bomb_rct):  # 練習５：ぶつかってたら
            print("ゲームオーバー")
            return

        screen.blit(bg_img, [0, 0])
        
        ####こうかとん####
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in delta.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 練習３：横方向の合計移動量
                sum_mv[1] += mv[1]  # 練習３：縦方向の合計移動量
        kk_rct.move_ip(sum_mv[0], sum_mv[1])  # 練習３：移動させる
        if check_bound(kk_rct) != (True, True):  # 練習４：はみだし判定
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        kk_img = kouka_houkou[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)  # 練習３：移動後の座標に表示させる
        
        ####爆弾####
        bomb_rct.move_ip(vx,vy) #練習問題２：爆弾を移動させる
        yoko,tate = check_bound(bomb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bomb, bomb_rct)#表示と座標の設定
        
        
        pg.display.update()
        tmr += 1
        clock.tick(60)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()