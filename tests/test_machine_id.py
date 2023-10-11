# Test scenario: Check that gym machines in input images are properly identified by the custom Rekognition model
import boto3
import os


# Positive tests: provide images that contain machines and ensure the system accurately identifies the machines.
# Returns the percentage of tests passed
def positive_test(path_images):
    model = ('arn:aws:rekognition:us-east-1:422292458603:project/gym_equipment/version/gym_equipment.2023-10-10T23.59'
             '.56/1696996796878')
    rekognition = boto3.client("rekognition", region_name='us-east-1')

    tests_passed = 0
    total = 0
    failed_tests = []

    for path in os.listdir(path_images):
        with open(f'{path_images}/{path}', 'r') as img:
            response = rekognition.detect_custom_labels(Image={'Bytes': img},
                                                        MinConfidence=50,
                                                        ProjectVersionArn=model)
            total += 1
            expected_tag = path[:path.index('.')]
            if len(response['CustomLabels']) > 0:
                if response['CustomLabels'][0]['Name'] == expected_tag:
                    tests_passed += 1
                else:
                    failed_tests.append(path)
            else:
                failed_tests.append(path)

    return total, tests_passed, failed_tests


# Negative tests: provide images that do not contain machines and ensure the system fails to return a label.
# Returns the percentage of tests passed
def negative_test(path_images):
    model = ('arn:aws:rekognition:us-east-1:422292458603:project/gym_equipment/version/gym_equipment.2023-10-10T23.59'
             '.56/1696996796878')
    rekognition = boto3.client("rekognition", region_name='us-east-1')

    tests_passed = 0
    total = 0
    failed_tests = []

    for path in os.listdir(path_images):
        with open(f'{path_images}/{path}', 'r') as img:
            response = rekognition.detect_custom_labels(Image={'Bytes': img},
                                                        MinConfidence=50,
                                                        ProjectVersionArn=model)
            total += 1
            if len(response['CustomLabels']) == 0:
                tests_passed += 1
            else:
                failed_tests.append(path)

    return total, tests_passed, failed_tests


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    negative_test_dataset = ''
    positive_test_dataset = ''

    # run tests
    positive_test_results = positive_test(positive_test_dataset)
    negative_test_results = negative_test(negative_test_dataset)

    # report results
    print(f'Positive testing results:')
    print(f'--------------------------')
    print(f'   Tests performed: {positive_test_results[0]}')
    print(f'   Tests passed: {positive_test_results[1]}')
    print(f'   Failed tests:')
    for failed_test in positive_test_results[2]:
        print(f'      {failed_test}')

    print(f'Negative testing results:')
    print(f'--------------------------')
    print(f'   Tests performed: {negative_test_results[0]}')
    print(f'   Tests passed: {negative_test_results[1]}')
    print(f'   Failed tests:')
    for failed_test in negative_test_results[2]:
        print(f'      {failed_test}')
