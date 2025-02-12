import random

import constants
from tree import Tree


class ParallaxManager:
    """
    Class to handle the background (hills and trees).
    """

    def __init__(self, grass_sprites, tree_sprites, mountain_sprites, sky_sprites):
        self.__left_offset = 0
        self.__right_offset = 0
        self.__sky_sprites = sky_sprites
        self.__grass_sprites = grass_sprites
        self.__grass_sprite_index = 0
        self.__mountain_sprites = mountain_sprites
        self.__tree_sprites = tree_sprites
        self.__trees = []

    def update(self, screen, player_speed, road, camera_offset_x):
        """
        Update the background based on player speed and road state.
        """
        if player_speed > 0:
            # Update existing trees

            for tree in self.__trees:
                tree.update(player_speed, road, camera_offset_x)

            # Remove trees that are no longer visible
            self.__trees = [tree for tree in self.__trees if tree.is_visible()]

            if len(self.__trees) < 3:
                self._generate_trees(road, camera_offset_x)

            self._update_grass(player_speed)
            self._update_mountains(road)

    def _generate_trees(self, road, camera_offset_x):
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

        self.__trees.append(Tree(self.__tree_sprites, position_x, side, depth, offset))

    def _update_grass(self, player_speed):

        if self.__grass_sprite_index >= 15:
            self.__grass_sprite_index = 0
        elif player_speed < 100:
            self.__grass_sprite_index += constants.FRAME_STEP_SLOW
        else:
            self.__grass_sprite_index += constants.FRAME_STEP

    def _update_mountains(self, road):
        if road is None:
            self.__left_offset = 0
            self.__right_offset = 0
        else:
            max_left_offset = (road.calculate_control_points(road.next_turn)['left'][1][0] -
                               road.calculate_control_points('straight')['left'][1][0]) * -1
            max_right_offset = (road.calculate_control_points(road.next_turn)['right'][1][0] -
                                road.calculate_control_points('straight')['right'][1][0]) * -1

            if self.__left_offset > max_left_offset:
                self.__left_offset -= constants.MOUNTAIN_PARALLAX_FACTOR
            elif self.__left_offset < max_left_offset:
                self.__left_offset += constants.MOUNTAIN_PARALLAX_FACTOR

            if self.__right_offset < max_right_offset:
                self.__right_offset += constants.MOUNTAIN_PARALLAX_FACTOR
            elif self.__right_offset > max_right_offset:
                self.__right_offset -= constants.MOUNTAIN_PARALLAX_FACTOR

    def render(self, screen):
        """
        Render the background elements.
        """
        screen.blit(self.__sky_sprites, (0, 0))
        screen.blit(self.__grass_sprites[int(self.__grass_sprite_index // constants.FRAME_FACTOR)], (0, 120))
        screen.blit(self.__mountain_sprites[0], (self.__left_offset, 0))
        screen.blit(self.__mountain_sprites[1], (self.__right_offset, 0))

        for tree in sorted(self.__trees, key=lambda x: x.depth, reverse=True):
            tree.render(screen)
