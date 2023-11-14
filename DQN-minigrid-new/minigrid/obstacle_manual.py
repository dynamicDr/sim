#!/usr/bin/env python3

from __future__ import annotations

import sys

sys.path.append(".")
sys.path.append("minigrid")

from minigrid.wrappers import ObstacleImgObsWrapper

import gymnasium as gym
import pygame
from gymnasium import Env

from core.actions import Actions
from minigrid_env import MiniGridEnv
from wrappers import ImgObsWrapper, RGBImgPartialObsWrapper



class ManualControl:
    def __init__(
        self,
        env: Env,
        seed=None
    ) -> None:
        self.env = env
        self.seed = seed
        self.closed = False
        self.run_time = 0
        self.slot_num = 0

    def start(self,slot_num=0):
        """Start the window display with blocking event loop"""
        self.slot_num=slot_num
        self.reset(self.seed)

        while not self.closed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.env.close()
                    break
                if event.type == pygame.KEYDOWN:
                    event.key = pygame.key.name(int(event.key))
                    self.key_handler(event)

    def step(self, action: Actions):
        obs, reward, terminated, truncated, _ = self.env.step(action)
        print(f"step={self.env.step_count}, reward={reward:.2f}")

        if terminated:
            print("terminated!")
            self.reset(self.seed)
        elif truncated:
            print("truncated!")
            self.reset(self.seed)
        else:
            self.env.render()

    def reset(self, seed=None):
        print(f"==================slotL{self.env.slot_num},run time:{self.run_time}==================")
        self.run_time+=1
        if self.run_time>1:
            self.closed=True
        self.env.reset(seed=seed)
        self.env.render()

    def key_handler(self, event):
        key: str = event.key
        print("pressed", key)

        if key == "escape":
            self.env.close()
            return
        if key == "backspace":
            self.reset()
            return

        key_to_action = {
            "left": Actions.left,
            "right": Actions.right,
            "up": Actions.forward,
            "1": Actions.toggle,
            "2": Actions.pickup,
            "3": Actions.drop,
            "tab": Actions.pickup,
            "left shift": Actions.drop,
            "enter": Actions.done,
        }
        if key in key_to_action.keys():
            action = key_to_action[key]
            self.step(action)
        else:
            print(key)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--env-id",
        type=str,
        help="gym environment to load",
        choices=gym.envs.registry.keys(),
        default="MiniGrid-MultiRoom-N6-v0",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="random seed to generate the environment with",
        default=None,
    )
    parser.add_argument(
        "--tile-size", type=int, help="size at which to render tiles", default=32
    )
    parser.add_argument(
        "--agent-view",
        action="store_true",
        help="draw the agent sees (partially observable view)",
    )
    parser.add_argument(
        "--agent-view-size",
        type=int,
        default=7,
        help="set the number of grid spaces visible in agent-view ",
    )
    parser.add_argument(
        "--screen-size",
        type=int,
        default="640",
        help="set the resolution for pygame rendering (width and height)",
    )

    args = parser.parse_args()
    for slot_num in [1,2,3,4,5]:

        env: MiniGridEnv = ObstacleImgObsWrapper(gym.make(
        args.env_id,
        tile_size=args.tile_size,
        render_mode="human",
        agent_pov=args.agent_view,
        agent_view_size=args.agent_view_size,
        screen_size=args.screen_size
        ),        env_name=args.env_id,slot_num=slot_num)


        manual_control = ManualControl(env, seed=args.seed)
        manual_control.start(slot_num=slot_num)
