# *********************************************************************
# This Original Work is copyright of 51 Degrees Mobile Experts Limited.
# Copyright 2019 51 Degrees Mobile Experts Limited, 5 Charlotte Close,
# Caversham, Reading, Berkshire, United Kingdom RG4 7BY.
#
# This Original Work is licensed under the European Union Public Licence (EUPL) 
# v.1.2 and is subject to its terms as set out below.
#
# If a copy of the EUPL was not distributed with this file, You can obtain
# one at https://opensource.org/licenses/EUPL-1.2.
#
# The 'Compatible Licences' set out in the Appendix to the EUPL (as may be
# amended by the European Commission) shall be deemed incompatible for
# the purposes of the Work and the provisions of the compatibility
# clause in Article 5 of the EUPL shall not apply.
# 
# If using the Work as, or as part of, a network application, by 
# including the attribution notice(s) required under Article 5 of the EUPL
# in the end user terms of the application under an appropriate heading, 
# such notice(s) shall fulfill the requirements of that article.
# ********************************************************************

## @example cloud/gettingstarted_console.py
# 
# @include{doc} example-getting-started-cloud.txt
# 
# This example is available in full on [GitHub](https://github.com/51Degrees/device-detection-python/blob/master/fiftyone_devicedetection_examples/fiftyone_devicedetection_examples/cloud/gettingstarted-console.py). 
# 
# @include{doc} example-require-resourcekey.txt
#
# Required PyPi Dependencies:
# - fiftyone_devicedetection
# 

import logging
import sys
from fiftyone_devicedetection.devicedetection_pipelinebuilder import DeviceDetectionPipelineBuilder
from fiftyone_devicedetection_examples.example_utils import ExampleUtils

class GettingStartedConsole():
    def run(self, resource_key, logger):

        # In this example, we use the DeviceDetectionPipelineBuilder
        # and configure it in code. For more information about
        # pipelines in general see the documentation at
        # http://51degrees.com/documentation/4.3/_concepts__configuration__builders__index.html        
        pipeline = DeviceDetectionPipelineBuilder(
            # Tell it that we want to use cloud and pass our resource key.
            resource_key = resource_key,
            # The origin header should be set in order to help the 
            # cloud service know where the request is coming from.
            cloud_request_origin = "51Degrees.example.com").build()

        # carry out some sample detections
        for values in self.EvidenceValues:
            self.analyseEvidence(values, pipeline, logger)

    def analyseEvidence(self, evidence, pipeline, logger):

        # FlowData is a data structure that is used to convey
        # information required for detection and the results of the
        # detection through the pipeline.
        # Information required for detection is called "evidence"
        # and usually consists of a number of HTTP Header field
        # values, in this case represented by a dictionary of header
        # name/value entries.
        data = pipeline.create_flowdata()
        
        message = []

        # List the evidence
        message.append("Input values:\n")
        for key in evidence:
            message.append(f"\t{key}: {evidence[key]}\n")
        
        logger.info("".join(message))

        # Add the evidence values to the flow data
        data.evidence.add_from_dict(evidence)

        # Process the flow data.
        data.process()

        message = []
        message.append("Results:\n")

        # Now that it's been processed, the flow data will have
        # been populated with the result. In this case, we want
        # information about the device, which we can get by
        # asking for a result matching named "device"
        device = data.device

        # Display the results of the detection, which are called
        # device properties. See the property dictionary at
        # https://51degrees.com/developers/property-dictionary
        # for details of all available properties.
        self.outputValue("Mobile Device", device.ismobile, message);
        self.outputValue("Platform Name", device.platformname, message);
        self.outputValue("Platform Version", device.platformversion, message);
        self.outputValue("Browser Name", device.browsername, message);
        self.outputValue("Browser Version", device.browserversion, message);
        logger.info("".join(message));

    def outputValue(self, name, value, message):
        # Individual result values have a wrapper called
        # `AspectPropertyValue`. This functions similarly to
        # a null-able type.
        # If the value has not been set then trying to access the
        # `value` method will throw an exception.
        # `AspectPropertyValue` also includes the `no_value_message`
        # method, which describes why the value has not been set.
        message.append(
            f"\t{name}: {value.value()}\n" if value.has_value()
            else f"\t{name}: {value.no_value_message()}\n")


    # This collection contains the various input values that will 
    # be passed to the device detection algorithm.
    EvidenceValues = [
        # A User-Agent from a mobile device.
        { "header.user-agent":
            "Mozilla/5.0 (Linux; Android 9; SAMSUNG SM-G960U) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "SamsungBrowser/10.1 Chrome/71.0.3578.99 Mobile Safari/537.36" },
        # A User-Agent from a desktop device.
        { "header.user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/78.0.3904.108 Safari/537.36" },
        # Evidence values from a windows 11 device using a browser
        # that supports User-Agent Client Hints.
        { "header.user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/98.0.4758.102 Safari/537.36",
            "header.sec-ch-ua-mobile": "?0",
        "header.sec-ch-ua":
            "\" Not A; Brand\";v=\"99\", \"Chromium\";v=\"98\", "
            "\"Google Chrome\";v=\"98\"",
            "header.sec-ch-ua-platform": "\"Windows\"",
            "header.sec-ch-ua-platform-version": "\"14.0.0\"" }
    ]

def main(argv):
    # Use the command line args to get the resource key if present.
    # Otherwise, get it from the environment variable.
    resource_key = argv[0] if len(argv) > 0 else ExampleUtils.get_resource_key() 
    
    # Configure a logger to output to the console.
    logger = logging.getLogger("Getting Started")
    logger.setLevel(logging.INFO)

    if (resource_key):
        GettingStartedConsole().run(resource_key, logger)
    else:
        logger.error(
            "No resource key specified in environment variable " +
            f"'{ExampleUtils.RESOURCE_KEY_ENV_VAR}'. The 51Degrees " +
            "cloud service is accessed using a 'ResourceKey'. " +
            "For more detail see " +
            "http://51degrees.com/documentation/4.3/_info__resource_keys.html. " +
            "A resource key with the properties required by this " +
            "example can be created for free at " +
            "https://configure.51degrees.com/g3gMZdPY. " +
            "Once complete, populated the environment variable " +
            "mentioned at the start of this message with the key.")

if __name__ == "__main__":
    main(sys.argv[1:])
