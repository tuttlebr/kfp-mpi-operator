# MPI Job as a Kubeflow Pipeline

Sample code and configurations to create a Kubeflow Pipeline which runs an MPIJob.

Kubernetes Resources Created:

1. **ServiceAccount**: Enables the creation of a service account under which the MPI Job will operate.
2. **RoleBinding**: Binds the Role defenition to the ServiceAccount
3. **Role**: Defines the access needed for the kubeflow namespace and the user's namespace to coordinate a pipeline and an MPI Job.
4. **MPIJob**: This defines the actual MPI job, MPI Operator is required to be installed on the Kubflow cluster.

## Create Kubeflow Pipeline Config

1. `docker-compse run` will build a container where a suitable KFP yaml will be constructed as defined in the `mpi-job.yaml` file.
2. The output will be two files:
   1. `create-*`: Config to create the resource via the Kubeflow pipelines GUI.
   2. `delete-*`: Config to delete the resource via the Kubeflow pipelines GUI. This is required for now as the pipeline workflow will not delete the MPI Job. If not deleted, the resources allocated to teh MPI job will remain allocated and unschedulable to other requests on the cluster.
3. Upload the two output files to the Kubeflow GUI, assign an experiment and create a run! This specific repo + mpirun will also create TensorBoard metadata which you can spin up within the Kubeflow Tensorboard gui.
