#!/usr/bin ptyhon
# -*- coding: utf-8 -*-
import infection

def main():
    # Total infection
    platform1 = infection.Platform(file = "user.json")
    platform1.infection(0, '1.0.1')
    platform1.infection(8, '1.2')
    platform1.infection(13, '1.1')
    platform1.infection(14, '2.0')
    platform1.printAllUsers()

    # Limited infection
    platform2 = infection.Platform(file = "user.json")
    print "Limited infection succeed?", platform2.limitedInfection(3, '1.0.1', 2)
    print "Limited infection succeed?", platform2.limitedInfection(3, '1.0.1', 4)
    print "Limited infection succeed?", platform2.limitedInfection(13, '1.1', 4)
    print "Limited infection succeed?", platform2.limitedInfection(15, '2.0', 1)


if __name__ == "__main__":
    main()
