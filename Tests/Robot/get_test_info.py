from ExtremeAutomation.Utilities.Framework.test_case_inventory import RobotTestData
import argparse
import json
import os

parser = argparse.ArgumentParser(description='Get info for Robot files.')
parser.add_argument('files',
                    type=str,
                    nargs='+',
                    help='a file to process')
args = parser.parse_args()

def main(path):
    TS = RobotTestData(path)
    output = TS.print_suite(TS.testsObj)
    print(f"qTest Tag Count: {TS.qTestTagCount}\nqTest Tags: {TS.qTestTags}")

    return output

if __name__ == '__main__':
    # main(sys.argv[1])
    output_dict = {}
    for file in args.files:
        result = main(file)
        # merge the result dict into the output dict
        output_dict = {**output_dict, **result}
        # output_dict[file] = result

    # Output CICD info
    print(json.dumps(output_dict))
    with open(f'{os.getcwd()}/robot_data.json', 'w') as outfile:
        json.dump(output_dict, outfile)