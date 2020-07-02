#! /usr/bin/env python

import os
import gcat_workflow_cloud.abstract_task as abstract_task

class Task(abstract_task.Abstract_task):
    CONF_SECTION = "melt"
    TASK_NAME = CONF_SECTION

    def __init__(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        super(Task, self).__init__(
            "melt-single.sh",
            param_conf.get(self.CONF_SECTION, "image"),
            param_conf.get(self.CONF_SECTION, "resource"),
            output_dir + "/logging"
        )
        
        self.task_file = self.task_file_generation(output_dir, task_dir, sample_conf, param_conf, run_conf)

    def task_file_generation(self, output_dir, task_dir, sample_conf, param_conf, run_conf):

        task_file = "{}/{}-tasks-{}-{}.tsv".format(task_dir, self.TASK_NAME, run_conf.get_owner_info(), run_conf.analysis_timestamp)
        with open(task_file, 'w') as hout:
            
            hout.write(
                '\t'.join([
                    "--input INPUT_BAM",
                    "--input INPUT_BAI",
                    "--output-recursive OUTPUT_DIR",
                    "--input-recursive REFERENCE_DIR",
                    "--env REFERENCE_FILE",
                ]) + "\n"
            )
            for sample in sample_conf.melt:
                hout.write(
                    '\t'.join([
                        "%s/cram/%s/%s.markdup.cram" % (output_dir, sample, sample),
                        "%s/cram/%s/%s.markdup.cram.crai" % (output_dir, sample, sample),
                        "%s/melt/%s" % (output_dir, sample),
                        param_conf.get(self.CONF_SECTION, "reference_dir"),
                        param_conf.get(self.CONF_SECTION, "reference_file"),
                    ]) + "\n"
                )

        return task_file