#! /usr/bin/env python

import gcat_workflow_cloud.abstract_task as abstract_task

class Task(abstract_task.Abstract_task):
    CONF_SECTION = "manta"
    TASK_NAME = CONF_SECTION

    def __init__(self, task_dir, sample_conf, param_conf, run_conf):

        super(Task, self).__init__(
            "manta-germline.sh",
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
                    "--input-recursive NORMAL_BAM_DIR",
                    "--env NORMAL_BAM_FILE",
                    "--output-recursive OUTPUT_DIR",
                    "--input-recursive  REFERENCE_DIR",
                    "--env  REFERENCE_FILE",
                    "--env CONFIG_MANTA_OPTION",
                    "--env WORKFLOW_OPTION",
                ]) + "\n"
            )
            for sample in sample_conf.manta:
                hout.write(
                    '\t'.join([
                        "%s/cram/%s" % (run_conf.output_dir, sample),
                        "%s.markdup.cram" % (sample),
                        "%s/manta/%s" % (run_conf.output_dir, sample),
                        param_conf.get(self.CONF_SECTION, "reference_dir"),
                        param_conf.get(self.CONF_SECTION, "reference_file"),
                        param_conf.get(self.CONF_SECTION, "manta_config_option"),
                        param_conf.get(self.CONF_SECTION, "manta_workflow_option") + " " + param_conf.get(self.CONF_SECTION, "manta_workflow_threads_option"),
                    ]) + "\n"
                )
        return task_file
