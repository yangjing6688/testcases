from ExtremeAutomation.Utilities.Framework.test_case_inventory import RobotTestData
import sys

def main(path):
    TS = RobotTestData(path)
    TS.print_suite(TS.testsObj)
    print(f"qTest Tag Count: {TS.qTestTagCount}\nqTest Tags: {TS.qTestTags}")

if __name__ == '__main__':
    main(sys.argv[1])