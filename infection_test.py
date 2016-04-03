#!/usr/bin ptyhon
# -*- coding: utf-8 -*-
import infection
import unittest
import argparse
import sys

class TestCompleteInfectionPlatform(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.platform1 = infection.Platform(file = "data/users_100.json")
        self.platform2 = infection.Platform(file = "data/users_10000.json")

    def testTotalInfection(self):
        self.platform1.infection(15, '1.0.1')
        self.platform1.infection(45, '1.2')
        self.platform1.infection(75, '2.0')
        self.assertEqual('1.0.1', self.platform1.getUserById(2).getVersion())
        self.assertEqual('1.2', self.platform1.getUserById(39).getVersion())
        self.assertEqual('2.0', self.platform1.getUserById(29).getVersion())
        # self.platform1.generateGraph()

        self.platform2.infection(4515, '1.0.1')
        self.platform2.infection(146, '1.2')
        self.platform2.infection(1463, '2.0')
        self.assertEqual('1.0.1', self.platform2.getUserById(897).getVersion())
        self.assertEqual('1.2', self.platform2.getUserById(176).getVersion())
        self.assertEqual('2.0', self.platform2.getUserById(526).getVersion())

    def testLimitedInfection(self):
        self.assertEqual(False, self.platform1.limitedInfection(64, '1.0.1', 15))
        self.assertEqual(True, self.platform1.limitedInfection(64, '1.0.1', 16))
        self.assertEqual(False, self.platform1.limitedInfection(98, '2.0.1', 10))
        self.assertEqual(True, self.platform1.limitedInfection(98, '2.0.1', 20))

        self.assertEqual(False, self.platform2.limitedInfection(5502, '1.0.1'), 50)
        self.assertEqual(True, self.platform2.limitedInfection(5502, '1.0.1'), 200)
        self.assertEqual(False, self.platform2.limitedInfection(6288, '2.0.1'), 5)
        self.assertEqual(True, self.platform2.limitedInfection(6288, '2.0.1'), 20)


class TestSimpleInfectionPlatform(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.platform = infection.Platform(file = "data/users_15.json")

    def testTotalInfection(self):
        # Simple Total infection
        self.platform.infection(0, '1.0.1')
        self.platform.infection(8, '1.2')
        self.platform.infection(13, '1.1')
        self.platform.infection(14, '2.0')
        self.assertEqual('1.0.1', self.platform.getUserById(5).getVersion())
        self.assertEqual('1.2', self.platform.getUserById(9).getVersion())
        self.assertEqual('1.1', self.platform.getUserById(10).getVersion())
        self.assertEqual('2.0', self.platform.getUserById(15).getVersion())

        # self.platform.generateGraph()

    def testLimitedInfection(self):
        # Limited infection
        self.assertEqual(False, self.platform.limitedInfection(3, '1.0.1', 2))
        self.assertEqual(False, self.platform.limitedInfection(3, '1.0.1', 4))
        self.assertEqual(True, self.platform.limitedInfection(13, '1.1', 4))
        self.assertEqual(False, self.platform.limitedInfection(15, '2.0', 1))

def main(argv):
    parser = argparse.ArgumentParser(description='Infection platform test')
    parser.add_argument('-type', type=str, default="simple", choices=["complete", "simple"])

    args = parser.parse_args(argv)

    suites = []
    if args.type == 'complete':
        suites.append(unittest.TestLoader().loadTestsFromTestCase(TestCompleteInfectionPlatform))
    suites.append(unittest.TestLoader().loadTestsFromTestCase(TestSimpleInfectionPlatform))
    for s in suites:
        unittest.TextTestRunner(verbosity=2).run(s)

if __name__ == "__main__":
    main(sys.argv[1:])
