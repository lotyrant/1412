#-*- coding:utf-8 -*-

import pygame
import random
from sys import exit
from pygame.locals import *
from model import *

# 画面の広さを設定する
SCREEN_WIDTH = 480
# 画面の高さを設定する
SCREEN_HEIGHT = 800


# ウィンドウをリセット
pygame.init()
# タイトル
pygame.display.set_caption("Hit Airplane")
# ウインドウの範囲
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# マウスポインタを隠す
pygame.mouse.set_visible(False)
font = pygame.font.SysFont("", 40)
text_surface = font.render("Hello", True, (0, 0, 255))
x = 0
y = (480 - text_surface.get_height()) / 2


# 背景画像
bg = pygame.image.load("resources/image/bg.png")
# ゲームオーバー画像
bg_game_over = pygame.image.load("resources/image/bg_game_over.png")
# ゲームイメージ
img_plane = pygame.image.load("resources/image/shoot.png")
img_start = pygame.image.load("resources/image/start.png")
img_pause = pygame.image.load("resources/image/pause.png")
# icon
img_icon = pygame.image.load("resources/image/plane.png").convert_alpha()
# ウインドウアイコン
pygame.display.set_icon(img_icon)

# 効果音
pygame.mixer.init()
sound_explosion = pygame.mixer.Sound("resources/audio/explosion.wav")
sound_shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
sound_game_over = pygame.mixer.Sound("resources/audio/bg_game_over.wav")
sound_explosion.set_volume(1)
sound_shoot.set_volume(0.5)
sound_game_over.set_volume(5)

#bgm
pygame.mixer.music.load("resources/audio/bg_game.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 飛行機
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))
player_rect.append(pygame.Rect(165, 360, 102, 126))
# 爆発イメージ
player_rect.append(pygame.Rect(165, 234, 102, 126))
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
# 出発点リセット
player_pos = [200, 600]

# プレイヤー作成
player = Player(img_plane, player_rect, player_pos)

# 弾
bullet_rect = pygame.Rect(1004, 987, 9, 21)
# 弾イメージ
bullet_img = img_plane.subsurface(bullet_rect)

# 敵
enemy_rect = pygame.Rect(534, 612, 57, 43)
# 敵イメージ
enemy_img = img_plane.subsurface(enemy_rect)
# 攻撃を受けたとき敵
enemy_explosion_imgs = []
enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(930, 697, 57, 43)))

# 敵スプライト
enemies = pygame.sprite.Group()
# 攻撃を受けたとき敵スプライト
enemies_explosion = pygame.sprite.Group()
# 攻撃頻度
shoot_frequency = 0
# 敵作成頻度
enemy_frequency = 0
# プレイヤーが攻撃を受けた時の表現順序
player_explosion_index = 16

score = 0
running = True
is_pause = False
is_game_over = False
clock = pygame.time.Clock()

# ゲームスタート
while running:

	# フレームレート　60に設定する
	clock.tick(60)

	# 一時停止
	if not is_pause and not is_game_over:

		if not player.is_hit:
			# 連続射撃設定する
			if shoot_frequency % 15 == 0:
				sound_shoot.play()
				player.shoot(bullet_img)

			shoot_frequency += 1
			# 頻度が１５を超えた時ゼロにリセットする
			if shoot_frequency >= 15:
				shoot_frequency = 0

		# 敵作成頻度
		if enemy_frequency % 50 == 0:
			# 敵現れ位置
			enemy_pos = [random.randint(0, SCREEN_WIDTH - enemy_rect.width), 0]
			enemy = Enemy(enemy_img, enemy_explosion_imgs, enemy_pos)
			enemies.add(enemy)

		enemy_frequency += 1
		if enemy_frequency >= 100:
			enemy_frequency = 0

		# 弾ルード設定
		for bullet in player.bullets:
			bullet.move()
			if bullet.rect.bottom < 0:
				player.bullets.remove(bullet)

		# 敵
		for enemy in enemies:
			enemy.move()
			# プレイヤーと接触かどうか
			if pygame.sprite.collide_circle(enemy, player):
				enemies_explosion.add(enemy)
				enemies.remove(enemy)
				player.is_hit = True
				# ゲームオーバー
				is_game_over = True
				# 効果音
				sound_game_over.play()

			# 敵が画面内かどうか
			if enemy.rect.top < 0:
				enemies.remove(enemy)

		# 敵と弾接触した場合
		enemy_explosion = pygame.sprite.groupcollide(enemies, player.bullets, 1, 1)
		for enemy in enemy_explosion:
			enemies_explosion.add(enemy)


 	# 画面
	screen.fill(0)
	# 背景入れ
	screen.blit(bg, (0, 0))
	author_font = pygame.font.SysFont("微软雅黑", 24)
	author_text = author_font.render("https://github.com/lotyrant/1412", True, (160, 160, 160))
	author_rect = author_text.get_rect();
	author_rect.centerx = SCREEN_WIDTH - 160
	author_rect.centery = SCREEN_HEIGHT - 20
	screen.blit(author_text, author_rect)


	# プレイヤー入れ
	if not player.is_hit:
		screen.blit(player.image[int(player.img_index)], player.rect)
		player.img_index = shoot_frequency / 8
	else:
		if player_explosion_index > 47:
			is_game_over = True
		else:
			player.img_index = player_explosion_index / 8
			screen.blit(player.image[int(player.img_index)], player.rect)
			player_explosion_index += 1


	# 攻撃を受けたとき敵
	for enemy in enemies_explosion:
		if enemy.explosion_index == 0:
			pass
		if enemy.explosion_index > 7:
			enemies_explosion.remove(enemy)
			# 効果音
			sound_explosion.play()
			score += 100
			continue
		# イメージ
		screen.blit(enemy.explosion_img[int(enemy.explosion_index / 2)], enemy.rect)
		enemy.explosion_index += 1


	# 弾を表示する
	player.bullets.draw(screen)
	# 敵を表示する
	enemies.draw(screen)

	# 点数表現分数
	score_font = pygame.font.Font(None, 36)
	score_text = score_font.render(str(score), True, (128, 128, 128))
  	# ヒントフレーム
	text_rect = score_text.get_rect()
	# ヒントの位置
	text_rect.topleft = [20, 10]
	# 点数を表示する
	screen.blit(score_text, text_rect)

	left, middle, right = pygame.mouse.get_pressed()
	# 一時停止
	if right == True and not is_game_over:
		is_pause = True

	if left == True:
		# ゲームリセット
		if is_game_over:
			is_game_over = False
			player_rect = []
			player_rect.append(pygame.Rect(0, 99, 102, 126))
			player_rect.append(pygame.Rect(165, 360, 102, 126))
			player_rect.append(pygame.Rect(165, 234, 102, 126))
			player_rect.append(pygame.Rect(330, 624, 102, 126))
			player_rect.append(pygame.Rect(330, 498, 102, 126))
			player_rect.append(pygame.Rect(432, 624, 102, 126))
			player = Player(img_plane, player_rect, player_pos)

			bullet_rect = pygame.Rect(1004, 987, 9, 21)
			bullet_img = img_plane.subsurface(bullet_rect)
			enemy_rect = pygame.Rect(534, 612, 57, 43)
			enemy_img = img_plane.subsurface(enemy_rect)
			enemy_explosion_imgs = []
			enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(267, 347, 57, 43)))
			enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(873, 697, 57, 43)))
			enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(267, 296, 57, 43)))
			enemy_explosion_imgs.append(img_plane.subsurface(pygame.Rect(930, 697, 57, 43)))

			enemies = pygame.sprite.Group()
			enemies_explosion = pygame.sprite.Group()
			score = 0
			shoot_frequency = 0
			enemy_frequency = 0
			player_explosion_index = 16

		# ゲーム再開
		if is_pause:
			is_pause = False

	font = pygame.font.SysFont("Meiryo", 40)
	if is_pause:
		screen.blit(img_start, (20, 50))
		text = font.render("Press Left Mouse to Continue", True, (255, 0, 0))
		text_rect = text.get_rect()
		text_rect.centerx = screen.get_rect().centerx
		text_rect.centery = screen.get_rect().centery
		screen.blit(text, text_rect)
	else:
		screen.blit(img_pause, (20, 50))
		hint_font = pygame.font.Font(None, 20)
		hint_text = hint_font.render("press right mount to pause", True, (128, 128, 128))
		text_rect = hint_text.get_rect()
		text_rect.topleft = [55, 55]
		screen.blit(hint_text, text_rect)


	# ゲームオーバー
	if is_game_over:
		font = pygame.font.SysFont("Meiryo", 48)
		text = font.render("Score: " + str(score), True, (255, 0, 0))
		text_rect = text.get_rect()
		text_rect.centerx = screen.get_rect().centerx
		text_rect.centery = screen.get_rect().centery + 70
		# ゲームオーバーを表示する
		screen.blit(bg_game_over, (0, 0))
		# 点数を表示する
		screen.blit(text, text_rect)

		font = pygame.font.SysFont("Meiryo", 40)
		text = font.render("Press Left Mouse to Restart", True, (255, 0, 0))
		text_rect = text.get_rect()
		text_rect.centerx = screen.get_rect().centerx
		text_rect.centery = screen.get_rect().centery + 150
		screen.blit(text, text_rect)


	# 画面をリロード
	pygame.display.update()

	# ゲーム脱出
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

	if not is_pause and not is_game_over:
		key = pygame.key.get_pressed()
		if key[K_w] or key[K_UP]:
			player.moveUp()
		if key[K_s] or key[K_DOWN]:
			player.moveDown()
		if key[K_a] or key[K_LEFT]:
			player.moveLeft()
		if key[K_d] or key[K_RIGHT]:
			player.moveRight()


while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()

	# 画面をリロード
	pygame.display.update()
