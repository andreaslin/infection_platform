#!/usr/bin ptyhon
# -*- coding: utf-8 -*-
import infection
import unittest
import argparse
import sys

class TestCompleteInfectionPlatform(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.platform = infection.Platform(file = "users_10000.json")

    def testTotalInfection(self):
        self.platform.generateGraph()

class TestSimpleInfectionPlatform(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.platform = infection.Platform(file = "users_15.json")

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
