# Text to SQL for Omics databases

This repository presents code that will accelerate you on your task to deploy a Text-to-SQL infrastructure to work
specifically with Omics data. Omics data refers to genes, variants, and diverse set of annotations around genomics
health care and life sciences field.

The GenAI-based application will offer a simple user interface that clinical scientists can use to
ask questions about genes and their variants in plain English that would allow them to discover
correlations between genes and disease efficiently.

---

<details open="open">
<summary>Table of Contents</summary>

- [About](#about)

</details>

---

## About

This repository maintains the artifacts necessary to:

1. Build the environment necessary to manage data, execute generative AI models, and provide a demonstration user interface
1. Deploy data to the various stores
1. Build and run a localhost user interface

Please follow the instructions on the specific README.md files in the following sequence:
1. [frontend](./frontend/README.md) for instructions on running the frontend user interface. This step must be executed before the `python-cdk` deployment.
1. [python-cdk](./python_cdk/README.md) for the CDK build and deploy. You will need to copy the Cognito User Pool ID and save in a configuration file for this step.

This sample code assumes you have the necessary permissions to create resources and execute scripts within at least one target AWS account.
