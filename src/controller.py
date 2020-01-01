from .model import Model
import numpy as np
import pygame
from pygame.locals import VIDEORESIZE
import time

TRANSPOSE = False
FPS = 30
SQUARE = 20
PREVIEW = 10

# In seconds
DESCENT_DELAY = 1
FAST_DESCENT_DELAY = 0.5

class Controller:
	def __init__(self, model: Model):
		self.model = model

		self.w, self.h = 10, 22

		pygame.init()

		self.video_size = [200 + SQUARE * self.w + 15, 15 + SQUARE * self.h + 15]
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(self.video_size)

		self.last_model_tick = 0
		self.game_start_time = 0

		self.font = pygame.font.SysFont("courier_new", 32, bold=True)

		self.main_frame = np.zeros((self.video_size[0], self.video_size[1], 3), dtype=np.uint8)

		squares = [[[40, 160], [48, 90]],
				   [[40, 160], [148, 190]],
				   [[70, 130], [240, 300]],
				   [[70, 130], [340, 400]]]
		thickness = 2

		for sqr in squares:
			self.main_frame[sqr[0][0]:sqr[0][1], sqr[1][0]:sqr[1][1], :] = 240
			self.main_frame[sqr[0][0]+thickness:sqr[0][1]-thickness, sqr[1][0]+thickness:sqr[1][1]-thickness, :] = 0

	def game(self):
		self.last_model_tick = time.time()
		self.game_start_time = time.time()

		while True:
			# Retrieving current state
			grid = self.model.grid
			score = self.model.score
			time_counter = self.model.time_counter
			held_tetro = self.model.held_tetro							# Tetro index
			current_tetro = self.model.current_tetro					# Tetro index
			current_tetro_position = self.model.current_tetro_position	# (X,Y) index of source
			current_tetro_rotation = self.model.current_tetro_rotation	# 0-3
			next_tetro = self.model.next_tetro							# Tetro index

			# grid = np.random.randint(0, 7, (22, 10), dtype=np.uint8)


			# --- Rendering current state ---
			rendered = self.render_state(grid)
			pyg_img = pygame.surfarray.make_surface(rendered.swapaxes(0, 1) if TRANSPOSE else rendered)
			self.screen.blit(pyg_img, (0, 0))

			game_time = round(time.time() - self.game_start_time)
			seconds = game_time % 60
			minutes = (game_time - seconds) // 60 % 60
			time_str = ("0" if minutes < 10 else "") + str(minutes) + ":" + ("0" if seconds < 10 else "") + str(seconds)
			time_text = self.font.render(time_str, True, (240, 240, 240))
			self.screen.blit(time_text, (100 - time_text.get_width() // 2, 70 - time_text.get_height() // 2))

			score_text = self.font.render(str(score), True, (240, 240, 240))
			self.screen.blit(score_text, (100 - score_text.get_width() // 2, 170 - score_text.get_height() // 2))

			next_tetro_render = self.render_grid(next_tetro.array * next_tetro.id, preview=True)
			pyg_img = pygame.surfarray.make_surface(next_tetro_render.swapaxes(0, 1) if TRANSPOSE else next_tetro_render)
			self.screen.blit(pyg_img, (100 - next_tetro_render.shape[1] // 2, 270 - next_tetro_render.shape[0] // 2))

			if held_tetro is not None:
				held_tetro_render = self.render_grid(held_tetro.array * held_tetro.id, preview=True)
				pyg_img = pygame.surfarray.make_surface(held_tetro_render.swapaxes(0, 1) if TRANSPOSE else held_tetro_render)
				self.screen.blit(pyg_img, (100 - held_tetro_render.shape[1] // 2, 370 - held_tetro_render.shape[0] // 2))


			# --- Checking events ---
			fast_descent = False
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN and (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
					self.model.hold()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
					self.model.instant_descent()
					self.last_model_tick = time.time()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
					self.model.rotate()
					self.last_model_tick = time.time()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
					self.model.left()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
					self.model.right()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
					fast_descent = True
				elif event.type == VIDEORESIZE:
					self.video_size = event.size
					self.screen = pygame.display.set_mode(self.video_size)

			# Passing to next frame
			pygame.display.flip()
			self.clock.tick(FPS)

			if time.time() - self.last_model_tick > (FAST_DESCENT_DELAY if fast_descent else DESCENT_DELAY):
				self.model.tick()
				self.last_model_tick = time.time()

	def render_state(self, grid):
		grid_start_x = 200
		grid_end_x = 200 + SQUARE * self.w
		grid_start_y = 15
		grid_end_y = 15 + SQUARE * self.h

		render = self.main_frame.copy()

		grid_render = self.render_grid(grid, rows=22)

		render[grid_start_x:grid_end_x, grid_start_y:grid_end_y, :] = np.swapaxes(grid_render, 0, 1)
		return render

	def render_grid(self, grid, rows=None, preview=False):
		if rows is not None:
			grid = grid[:rows, :]
		size = PREVIEW if preview else SQUARE

		T_color = [200, 0, 200]
		L_color = [240, 150, 0]
		J_color = [30, 30, 255]
		O_color = [240, 240, 20]
		Z_color = [240, 30, 30]
		S_color = [30, 240, 30]
		I_color = [0, 100, 200]
		tetros = [Model.TETRO_T.id, Model.TETRO_L.id, Model.TETRO_J.id, Model.TETRO_O.id,
				  Model.TETRO_Z.id, Model.TETRO_S.id, Model.TETRO_I.id]
		tetro_colors = [T_color, L_color, J_color, O_color, Z_color, S_color, I_color]

		grid = np.repeat(grid[:, :, np.newaxis], 3, axis=2)
		grid_render = np.zeros((grid.shape[0], grid.shape[1], 3), dtype=np.uint8)
		for tetro, color in zip(tetros, tetro_colors):
			grid_render[:, :, :] += (grid == tetro) * np.array(color, dtype=np.uint8)
		grid_render = np.kron(grid_render, np.ones((size, size, 1), dtype=np.uint8))

		return grid_render



# TETROMINI: T L J O Z S I