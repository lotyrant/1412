import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

# 弾
class Bullet(pygame.sprite.Sprite):
	
	def __init__(self, img, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		# イメージ範囲
		self.rect = self.image.get_rect()
		self.rect.midbottom = pos
		self.speed = 10

	def move(self):
		self.rect.top -= self.speed


# 敵
class Enemy(pygame.sprite.Sprite):
	
	def __init__(self, img, explosion_img, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.topleft = pos
		self.explosion_img = explosion_img
		self.speed = 2
		# 攻撃を受けた時
		self.explosion_index = 0

	def move(self):
		# 敵弾方向
		self.rect.top += self.speed


# プレイヤー
class Player(pygame.sprite.Sprite):

	def __init__(self, img, rect, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = []
		# 飛行機イメージ処理
		for i in range(len(rect)):
			self.image.append(img.subsurface(rect[i]).convert_alpha())
		# 飛行機範囲
		self.rect = rect[0]
		self.rect.topleft = pos
		self.speed = 8
		# スプライト実例
		self.bullets = pygame.sprite.Group()
		self.img_index = 0
		# 攻撃判断
		self.is_hit = False

	def shoot(self, img):
		bullet = Bullet(img, self.rect.midtop)
		# 弾実例
		self.bullets.add(bullet)

	def moveUp(self):
		# 一番上
		if self.rect.top <= 0:
			self.rect.top = 0
		else:
			self.rect.top -= self.speed

	def moveDown(self):
		# 一番底辺
		if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
			self.rect.top = SCREEN_HEIGHT - self.rect.height
		else:
			self.rect.top += self.speed

	def moveLeft(self):
		# 一番左
		if self.rect.left <= 0:
			self.rect.left = 0
		else:
			self.rect.left -= self.speed

	def moveRight(self):
		# 一番右
		if self.rect.left >= SCREEN_WIDTH - self.rect.width:
			self.rect.left = SCREEN_WIDTH - self.rect.width
		else:
			self.rect.left += self.speed

		


