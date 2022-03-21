"""Python script to define a Kubeflow pipeline.
MPIJob wrapped in a Kubeflow ResourceOp compiles the single-component pipeline. 
Included two ResourceOps which will create the pipeline and then delete the
pipeline when the user has completed their training. 
"""
import uuid
from os import getenv
import kfp
from kfp.components import create_component_from_func
import yaml

UNIQUE_ID = str(uuid.uuid1())[0:8]
UNIQUE_NAME = "{}-{}".format(getenv("KFP_NAME"), UNIQUE_ID)


@kfp.dsl.pipeline(
    name=UNIQUE_NAME,
    description=getenv("KFP_DSCR"),
)
class MPIOp:
    def __init__(self, unique_id, unique_name):
        self.unique_id = unique_id
        self.unique_name = unique_name

        stream = open("mpi-job.yaml", "rb")
        gen = yaml.load_all(stream, Loader=yaml.Loader)
        self.mpi_job = next(gen)
        for d in gen:
            self.mpi_job.update(d)

        self.mpi_job["metadata"]["name"] = self.unique_name

    def create_op(self):
        op = kfp.dsl.ResourceOp(
            action="create",
            name=self.unique_name,
            k8s_resource=self.mpi_job,
        )

    def delete_op(self):
        op = kfp.dsl.ResourceOp(
            name=self.unique_name,
            k8s_resource=self.mpi_job,
        ).delete()


if __name__ == "__main__":

    mpi_op = MPIOp(UNIQUE_ID, UNIQUE_NAME)

    kfp.compiler.Compiler().compile(
        mpi_op.create_op, "create-" + mpi_op.unique_name + ".yaml"
    )
    kfp.compiler.Compiler().compile(
        mpi_op.delete_op, "delete-" + mpi_op.unique_name + ".yaml"
    )

    print("Saved configs as *-{}.yaml".format(mpi_op.unique_name))
