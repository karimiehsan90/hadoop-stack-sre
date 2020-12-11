# hadoop-stack-sre

This project can help your deployment for the Hadoop stack.
You can use project docker images, helm charts,
and ansible roles to deploy the Hadoop stack on your cluster.
At the root of the project,
we have directories for each framework in the Hadoop stack.

In each directory, we have some directories for each deployment technology.
Now we just support docker files,
but we have plans to support ansible roles and helm charts.
After merging each pull request to the main branch,
the built docker images will push to the docker hub.

You can pull our docker images in this syntax:

```bash
docker pull karimiehsan90/${FRAMEWORK_NAME}:${FRAMEWORK_VERSION}
```

For example, to pull the Hadoop docker image you can run the below script:

```bash
docker pull karimiehsan90/hadoop:2.7.7
```

# Contribution guide

We'll so happy for your contribution and
any contribution to the Hadoop stack deployment will be reviewed and then merged.

We're waiting for your pull requests.
