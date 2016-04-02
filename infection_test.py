#!/usr/bin ptyhon
# -*- coding: utf-8 -*-
import infection

def main():
    # quick test, should not do this in real work
    platform = infection.Platform(file = "user.json")
    platform.infection(0, '1.0.1')
    platform.infection(8, '1.2')
    platform.infection(13, '1.1')
    platform.infection(14, '2.0')

    platform.printAllUsers()

if __name__ == "__main__":
    main()
