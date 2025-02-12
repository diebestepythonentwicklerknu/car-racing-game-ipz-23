import random

import constants
from tree import Tree


class ParallaxManager:
    """
    Class to handle the background (hills and trees).
    """

    def __init__(self, grass_sprites, tree_sprites, mountain_sprites, sky_sprites):
        self.left_offset = 0
        self.right_offset = 0
        self.sky_sprites = sky_sprites
        self.grass_sprites = grass_sprites
        self.grass_sprite_index = 0
        self.mountain_sprites = mountain_sprites
        self.tree_sprites = tree_sprites
        self.trees = []

    def update(self, screen, player_speed, road, camera_offset_x):
        """
        Update the background based on player speed and road state.
        """
        if player_speed > 0:
            # Update existing trees

            for tree in self.trees:
                tree.update(player_speed, road, camera_offset_x)

            # Remove trees that are no longer visible
            self.trees = [tree for tree in self.trees if tree.is_visible()]

            if len(self.trees) < 3:
                self.generate_trees(road, camera_offset_x)

            self.update_grass(player_speed)
            self.update_mountains(road)

    def generate_trees(self, road, camera_offset_x):
        # Generate new trees randomly if fewer than 3 are visible

        side = random.choice(['left', 'right'])
        if road.next_turn == "hard_left" and side == 'left':
            return
        if road.next_turn == "hard_right" and side == 'right':
            return

        # Generate trees relative to the road's curvature
        depth = random.uniform(1.0, 1.2)
        lane_edges, y_position = road.get_lane_positions(depth, camera_offset_x)
        offset = random.randint(10, 200)  # Fixed offset range

        if side == 'left':
            if int(lane_edges[0]) - offset > 0:
                position_x = random.randint(0, int(lane_edges[0]) - offset)
            else:
                return
        elif int(lane_edges[-1]) + offset < constants.SCREEN_WIDTH - 1:
            position_x = random.randint(int(lane_edges[-1]) + offset, constants.SCREEN_WIDTH)
        else:
            return

        self.trees.append(Tree(self.tree_sprites, position_x, side, depth, offset))

    def update_grass(self, player_speed):

        if self.grass_sprite_index >= 15:
            self.grass_sprite_index = 0
        elif player_speed < 100:
            self.grass_sprite_index += constants.FRAME_STEP_SLOW
        else:
            self.grass_sprite_index += constants.FRAME_STEP

    def update_mountains(self, road):
        if road is None:
            self.left_offset = 0
            self.right_offset = 0
        else:
            max_left_offset = (road.calculate_control_points(road.next_turn)['left'][1][0] -
                               road.calculate_control_points('straight')['left'][1][0]) * -1
            max_right_offset = (road.calculate_control_points(road.next_turn)['right'][1][0] -
                                road.calculate_control_points('straight')['right'][1][0]) * -1

            if self.left_offset > max_left_offset:
                self.left_offset -= constants.MOUNTAIN_PARALLAX_FACTOR
            elif self.left_offset < max_left_offset:
                self.left_offset += constants.MOUNTAIN_PARALLAX_FACTOR

            if self.right_offset < max_right_offset:
                self.right_offset += constants.MOUNTAIN_PARALLAX_FACTOR
            elif self.right_offset > max_right_offset:
                self.right_offset -= constants.MOUNTAIN_PARALLAX_FACTOR

    def render(self, screen):
        """
        Render the background elements.
        """
        screen.blit(self.sky_sprites, (0, 0))
        screen.blit(self.grass_sprites[int(self.grass_sprite_index // constants.FRAME_FACTOR)], (0, 120))
        screen.blit(self.mountain_sprites[0], (self.left_offset, 0))
        screen.blit(self.mountain_sprites[1], (self.right_offset, 0))

        for tree in sorted(self.trees, key=lambda x: x.depth, reverse=True):
            tree.render(screen)
