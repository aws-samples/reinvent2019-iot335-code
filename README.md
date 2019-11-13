## Code snippets for re:Invent 2019 chalk talk "Implementing multi-region AWS IoT - IOT335"

Some code snippets for the re:Invent 2019 chalk talk **IOT335 - Implementing multi-region AWS IoT**

* The folder `jupyter` contains some Jupyter notebooks to create a PCA in ACM, register the CA with AWS IoT in 2 regions, register devices with JITR and replicate the device setup to another region and examples to persist data across regions
* The folder `cfn` contains CloudFormation templates for an IoT multi-region setup
* The folder `lambda` contains some lambda functions for Just-in-Time registration, DynamoDB trigger and step functions

To get started copy all files from the folder `jupyter` to a device (laptop, VM) where the Jupyter software is installed. You can use for example an [Amazon SageMaker notebook instance](https://docs.aws.amazon.com/sagemaker/latest/dg/nbi.html) which is easy to setup and to use. 

Go through all the notebooks in chronological order. They contain code as well as instructions.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.