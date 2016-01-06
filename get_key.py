#!/usr/bin/env python
# gey_key.py
# Get keystrokes from keyboard

import pygame

k = pygame.key.get_pressed()

if (k == K_A):
    print 'A'