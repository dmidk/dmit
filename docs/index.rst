dmit documentation
===============================

  .. toctree::
     :maxdepth: 1
     :hidden:

     install
     modules

=====
dmit
=====
*dmit* is a small package which collects mainly meteorological tools to avoid replicating code.

How to use?
-------------------------------
Just install and import where needed.

.. code-block:: python

   import dmit


Prerequisites
-------------------------------
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
