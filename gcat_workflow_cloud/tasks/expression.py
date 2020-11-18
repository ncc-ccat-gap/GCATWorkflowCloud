#! /usr/bin/env python

import gcat_workflow_cloud.abstract_task as abstract_task

class Task(abstract_task.Abstract_task):
    CONF_SECTION = "expression"
    TASK_NAME = CONF_SECTION

    def __init__(self, task_dir, sample_conf, param_conf, run_conf):

        super(Task, self).__init__(
            "expression.sh",
            param_conf.get(self.CONF_SECTION, "image"),
            param_conf.get(self.CONF_SECTION, "resource"),
            run_conf.output_dir + "/logging"
        )
        
        self.task_file = self.task_file_generation(task_dir, sample_conf, param_conf, run_conf)

    def task_file_generation(self, task_dir, sample_conf, param_conf, run_conf):

        task_file = "{}/{}-tasks-{}.tsv".format(task_dir, self.TASK_NAME, run_conf.project_name)
        with open(task_file, 'w') as hout:
            
            hout.write(
                '\t'.join([
                    "--input INPUT_CRAM",
                    "--output-recursive OUTPUT_DIR",
                    "--input REFERENCE",
                    "--input REFERENCE_INDEX",
                    "--input GTF",
                    "--env SAMPLE",
                ]) + "\n"
            )
            for sample in sample_conf.expression:
                hout.write(
                    '\t'.join([
                        "%s/cram/%s/%s.Aligned.sortedByCoord.out.cram" % (run_conf.output_dir, sample, sample),
                        "%s/expression/%s" % (run_conf.output_dir, sample),
                        param_conf.get(self.CONF_SECTION, "reference"),
                        param_conf.get(self.CONF_SECTION, "reference_index"),
                        param_conf.get(self.CONF_SECTION, "gtf"),
                        sample,
                    ]) + "\n"
                )
        return task_file
