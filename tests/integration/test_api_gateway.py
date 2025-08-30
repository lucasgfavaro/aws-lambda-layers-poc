import os

import boto3
import pytest
import requests

"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going to test. 
"""


class TestApiGateway:

    @pytest.fixture()
    def api_gateway_url(self):
        """ Get the API Gateway URL from Cloudformation Stack outputs """
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")

        if stack_name is None:
            raise ValueError('Please set the AWS_SAM_STACK_NAME environment variable to the name of your stack')

        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name} \n" f'Please make sure a stack with the name "{stack_name}" exists'
            ) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "HelloWorldApi"]

        if not api_outputs:
            raise KeyError(f"HelloWorldAPI not found in stack {stack_name}")

        return api_outputs[0]["OutputValue"]  # Extract url from stack outputs

    def test_api_gateway_hello_world_1(self, api_gateway_url):
        """ Call the API Gateway endpoint for hello-world-1 and check the response """
        # Replace /hello/ with /hello-world-1 in the URL
        url = api_gateway_url.replace("/hello/", "/hello-world-1")
        response = requests.get(url)

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "hello world 1"
        assert "sharedService" in data
        assert data["sharedService"] == "Layer working!"

    def test_api_gateway_hello_world_2(self, api_gateway_url):
        """ Call the API Gateway endpoint for hello-world-2 and check the response """
        # Replace /hello/ with /hello-world-2 in the URL
        url = api_gateway_url.replace("/hello/", "/hello-world-2")
        response = requests.get(url)

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "hello world 2"
        assert "sharedService" in data
        assert data["sharedService"] == "Layer working!"
