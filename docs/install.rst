============
Installation
============

------------
Requirements
------------
* Linux environment / MacOS with python3. This has not been tested on Windows. Python2 has not been tested either. It might work, but I will not test it.

------------
Installation
------------
You can install the package directly from pypi:

* **pip install dmit**

=============
Prerequisites
=============
To use the AWS S3 utility (part of the dmitio class) one needs to set the following environment variables:
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY
  - AWS_DEFAULT_REGION
  - AWS_S3_BUCKET
For bash an example could be (values are random and will not work!):
  - export AWS_ACCESS_KEY_ID="AJIEPXNW32N3A23APW3C"
  - export AWS_SECRET_ACCESS_KEY="XOnfa5HA+gwGEcC3ajklQ3kxlr3qXRR3s3k2xMaA"
  - export AWS_DEFAULT_REGION="eu-central-1"
  - export AWS_S3_BUCKET="my-bucket-name"