import allure
import pytest
import re

from flask import url_for


def _attach_screenshot(response):
    content = response.data
    filename = re.search(pattern=fr"filename=(?P<filename>.*\.png)",
                         string=response.headers["Content-Disposition"]).group("filename")
    if content:
        allure.attach(content,
                      name=filename,
                      attachment_type=allure.attachment_type.PNG)


@pytest.mark.usefixtures("start_stream")
def test_get_screenshot(client, video_stream_host, video_stream_port):
    expected_mimetype = "image/png"
    expected_status_code = 200

    description = f"""
    Test case to verify that a screenshot can be retrieved from an existing video stream.

    [Preconditions]
    1. Video stream is running on {video_stream_host} host and {video_stream_port} port.

    [Steps]
    1. Send a GET request to the screenshot endpoint with the video stream host and port.
    2. Verify the response status code.
    3. Verify the response content type.
    4. Verify the response data.

    [Expected Results]
    1. GET request is successfully sent.
    2. Response status code is {expected_status_code}.
    3. Response content type is '{expected_mimetype}'.
    4. Response data is not empty.
    """
    allure.dynamic.description(description)

    with allure.step("Retrieve a screenshot from the video stream"):
        response = client.get(url_for("screenshot_api.get_screenshot",
                                      port=video_stream_port,
                                      host=video_stream_host))

    with allure.step(f"Verify response status code ({expected_status_code})"):
        assert response.status_code == expected_status_code, \
            f"Expected status code {expected_status_code}, but got {response.status_code}"

    _attach_screenshot(response=response)

    with allure.step(f"Verify response content type ({expected_mimetype})"):
        assert response.mimetype == expected_mimetype, \
            f"Expected content type '{expected_mimetype}', but got {response.mimetype}"

    with allure.step("Verify screenshot data is not empty"):
        assert response.data, \
            "Expected screenshot data to be non-empty, but it is empty"


@pytest.mark.usefixtures("start_stream")
def test_get_multiple_screenshots(client, video_stream_host, video_stream_port):
    captured_screenshots = set()
    expected_screenshots_number = 5
    description = f"""
    Test case to verify that multiple unique screenshots can be retrieved from an existing video stream.
    
    [Preconditions]
    1. Video stream is running on {video_stream_host} host and {video_stream_port} port.
    
    [Steps]
    1. Send {expected_screenshots_number} GET requests to the screenshot endpoint with the video stream host and port.
    2. Verify that all screenshots are unique.

    [Expected Results]
    1. All {expected_screenshots_number} GET requests are successfully sent and screenshots are retrieved.
    2. All retrieved screenshots are unique.
    """
    allure.dynamic.description(description)

    with allure.step(f"Retrieve {expected_screenshots_number} screenshots from the video stream"):
        for i in range(expected_screenshots_number):
            with allure.step(f"Retrieve screenshot #{i + 1}"):
                response = client.get(url_for("screenshot_api.get_screenshot",
                                              port=video_stream_port,
                                              host=video_stream_host))
                assert response.status_code == 200, \
                    f"Failed to retrieve screenshot #{i + 1}, status code: {response.status_code}"
                _attach_screenshot(response=response)
                captured_screenshots.add(response.data)

    with allure.step("Verify that all screenshots are unique"):
        actual_screenshots_number = len(captured_screenshots)
        assert actual_screenshots_number == expected_screenshots_number, \
            (f"Expected to retrieve {expected_screenshots_number} unique screenshots,"
             f" but got less or more: {actual_screenshots_number}")



def test_get_screenshot_from_non_existing_stream(client, video_stream_host, video_stream_port):
    expected_status_code = 500
    description = f"""
    Test case to verify that a screenshot cannot be retrieved from a non-existing video stream.

    [Preconditions]
    1. Video stream is not running on {video_stream_host} host and {video_stream_port} port.

    [Steps]
    1. Send a GET request to the screenshot endpoint with the video stream host and port.
    2. Verify the response status code.

    [Expected Results]
    1. GET request is successfully sent.
    2. Response status code is {expected_status_code}, indicating that the screenshot cannot be retrieved.
    """
    allure.dynamic.description(description)

    with allure.step("Retrieve a screenshot from a non-existing video stream"):
        response = client.get(url_for("screenshot_api.get_screenshot",
                                      port=video_stream_port,
                                      host=video_stream_host))

    with allure.step(f"Verify the response status code ({expected_status_code})"):
        assert response.status_code == expected_status_code, \
            f"Expected status code to be {expected_status_code}, but got {response.status_code}"


def test_get_screenshot_invalid_port(client, video_stream_host):
    expected_status_code = 400
    description = f"""
    Test case to verify that a screenshot cannot be retrieved when the port is incorrect.

    [Steps]
    1. Send a GET request to the screenshot endpoint with the video stream host and an invalid port (e.g. non-integer).
    2. Verify the response status code.

    [Expected Results]
    1. GET request is successfully sent.
    2. Response status code is {expected_status_code}, indicating that the port is invalid.
    """
    allure.dynamic.description(description)

    with allure.step("Retrieve a screenshot with an invalid port"):
        response = client.get(url_for("screenshot_api.get_screenshot",
                                       port="invalid",
                                       host=video_stream_host))

    with allure.step(f"Verify the response status code ({expected_status_code})"):
        assert response.status_code == expected_status_code, \
            f"Expected status code to be {expected_status_code}, but got {response.status_code}"
