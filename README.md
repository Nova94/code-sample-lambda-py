# code sample lambda py
##### _also known as Lambda+Python K-V store example_
This project builds a serverless K-V store using AWS APIGateway, Lambda, and DynamoDB.

## Getting Started

### Prerequisites

The following should be installed before building the project.

* python 3.6.5 
* [awscli](https://docs.aws.amazon.com/cli/latest/userguide/installing.html)
* [serverless](https://serverless.com/framework/docs/getting-started/) >=1.12.0 <2.0.0 
* [serverless-python-requirements](https://github.com/UnitedIncome/serverless-python-requirements#install)

## Deployment

deploy with `make`  (runs unit tests first) or `make deploy` - it will deploy a cloudformation stack using serverless

End with an example of getting some data out of the system or using it for a little demo

`make remove` - destroys the cloudformation stack

## Running the tests

simply run - `make test` for unit tests

run the following command after a deploy to run through acceptance tests.

Service Endpoint and test-key are outputted during the deploy phase.

```
make acceptance endpoint={Service Endpoint} apikey={test-key}
```

## Built With

* [boto3](http://boto3.readthedocs.io/en/latest/index.html) - The AWS SDK for python
* [pip](https://pypi.org/project/pip/) - Dependency Management
* [pytest](https://docs.pytest.org/en/latest/) - Testing Framework

## Contributing

Not really open for contributing at this time. It is just a code sample for people to look at.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors
* **[Lisa Gray](linkedin.com/in/gray7)** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
