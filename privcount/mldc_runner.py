import logging
import os
import yaml

from time import time, sleep
from multiprocessing import Process, Queue
from Queue import Empty

from privcount.config import normalise_path
from privcount.data_collector import DataCollector

from onionpop.pipeline import Model

# this function is called in a new process
def run_data_collector(dc_rundir_path, dc_config_path, dc_id, req_q, res_q):
    # TODO make log file configurable and separate for each subproc?

    os.chdir(dc_rundir_path)
    dc = DataCollector(dc_config_path)
    # req_q is where the dc will send prediction requests
    # res_q is where the MLDCRunner will send responses
    dc.set_machine_learning_pipes(dc_id, req_q, res_q)
    dc.run()

class MLDCRunner(object):

    def __init__(self, config_filepath):
        # make sure config file exists
        if config_filepath is not None:
            path = normalise_path(config_filepath)
            if os.path.exists(path):
                self.config_filepath = path
            else:
                logging.warning("unable to initialize MLDCRunner: config file does not exist at path {}".format(path))
                return None

        # init some other class variables
        self.config = None

        self.position_model_path = None
        self.purpose_model_path = None
        self.webpage_model_path = None

        self.position_model = None
        self.purpose_model = None
        self.webpage_model = None

        # incoming work queue for predictions we need to make
        self.inq = None

        # holds mapping from dc_id to the q we use for prediction responses
        self.dcqmap = {}
        # holds mapping from dc_id to dc process object
        self.dcpmap = {}

        self.last_check_should_stop_time = None
        self.num_tasks_processed = 0

    def run(self):
    	try:
    	    self._run()
    	except KeyboardInterrupt:
    	    # ctrl-c
    	    logging.info("attempting to shut down gracefully")
            for dc_id in self.dcpmap:
                proc = self.dcpnap[dc_id]
                if proc is not None:
                    proc.terminate()
    	    self._cleanup()

    def _run(self):
        config = None
        with open(self.config_filepath, 'r') as fin:
            config = yaml.load(fin)

        # make sure the config is OK
        if config is not None and self._validate_config(config):
            self.config = config
        else:
            logging.warning("config contained invalid options, please try again")
            return

        # prepare (train) the models immediately if they are specified
        self._prepare_models()

        # if we have at least one model, we will need to faciliate predictions
        if self.position_model is not None or \
            self.purpose_model is not None or \
            self.webpage_model is not None:
            self.inq = Queue()

        # start all data collectors
        self._start_data_collectors()

        # now run the main loop
        self._loop()

        # cleanup
        self._cleanup()

    def _validate_config(self, candidate_config):
        if candidate_config is None:
            logging.warning("config is None")
            return False

        # 'dcs' is required
        if 'dcs' not in candidate_config:
            logging.warning("'dcs' are a required config element but is missing from the config file")
            return False

        # we need at least one 'dc'
        if len(candidate_config['dcs']) < 1:
            logging.warning("we need at least one entry in the 'dcs' config to run")
            return False

        # check for correct 'config' and 'rundir' k-v pairs in each entry
        for entry in candidate_config['dcs']:
            if 'config' not in entry or 'rundir' not in entry:
                logging.warning("each entry in the list of 'dcs' requires both a 'config' and 'rundir' key-value pair")
                return False

        # check that config and rundir paths exist
        for entry in candidate_config['dcs']:
            dc_conf_file_path = entry['config']

            if not os.path.exists(normalise_path(dc_conf_file_path)):
                logging.warning("entry in 'dcs' missing config file at path {}".format(dc_conf_file_path))
                return False

            dc_run_dir_path = entry['rundir']

            if not os.path.exists(normalise_path(dc_run_dir_path)):
                logging.warning("entry in 'dcs' missing rundir directory at path {}".format(dc_run_dir_path))
                return False

        # specifying the machine learning models is optional
        # but if the paths are specified, then files should exist
        if 'position_model' in candidate_config:
            conf_path = candidate_config['position_model']

            if not os.path.exists(normalise_path(conf_path)):
                logging.warning("'position_model' was given but no file exists at path {}".format(conf_path))
                return False

        if 'purpose_model' in candidate_config:
            conf_path = candidate_config['purpose_model']

            if not os.path.exists(normalise_path(conf_path)):
                logging.warning("'purpose_model' was given but no file exists at path {}".format(conf_path))
                return False

        if 'webpage_model' in candidate_config:
            conf_path = candidate_config['webpage_model']

            if not os.path.exists(normalise_path(conf_path)):
                logging.warning("'webpage_model' was given but no file exists at path {}".format(conf_path))
                return False

        # everything is OK
        return True

    def _prepare_models(self):
        logging.info("preparing machine learning models now")

        if 'position_model' in self.config:
            self.position_model_path = normalise_path(self.config['position_model'])
            config = {
                "dataset": self.position_model_path,
                "classifier": "PositionClassifier",
                "params": {"n_estimators": 30}
            }
            logging.info("loading machine learning position model")
            self.position_model = Model(config)
            logging.info("training machine learning position model")
            self.position_model.train()
            logging.info("finished preparing machine learning position model")

        if 'purpose_model' in self.config:
            self.purpose_model_path = normalise_path(self.config['purpose_model'])
            config = {
                "dataset": self.purpose_model_path,
                "classifier": "PurposeClassifier",
                "params": {"n_estimators": 30}
            }
            logging.info("loading machine learning purpose model")
            self.purpose_model = Model(config)
            logging.info("training machine learning purpose model")
            self.purpose_model.train()
            logging.info("finished preparing machine learning purpose model")

        if 'webpage_model' in self.config:
            self.webpage_model_path = normalise_path(self.config['webpage_model'])
            config = {
                "dataset": self.webpage_model_path,
                "classifier": "OneClassCUMUL",
                "params": {"nu": 0.2, "kernel": "rbf", "gamma": 10}
            }
            logging.info("loading machine learning webpage model")
            self.webpage_model = Model(config)
            logging.info("training machine learning webpage model")
            self.webpage_model.train()
            logging.info("finished preparing machine learning webpage model")

    def _start_data_collectors(self):
        logging.info("creating and starting child data collector processes now")
        dc_id = 0
        for entry in self.config['dcs']:
            dc_config_path = normalise_path(entry['config'])
            dc_rundir_path = normalise_path(entry['rundir'])

            # dc will send us requests in our inq
            dc_outq = self.inq
            # we will send responses to dc queries
            dc_inq = Queue() if dc_outq is not None else None

            # store the q map so we know which queue to send the response for each request
            self.dcqmap[dc_id] = dc_inq

            # setup a process to run the DC
            self.dcpmap[dc_id] = Process(target=run_data_collector, name="dc{}".format(dc_id),
                args=(dc_rundir_path, dc_config_path, dc_id, self.inq, dc_inq))

            # lets run it
            self.dcpmap[dc_id].start()

            logging.info("started proc {} id {}".format(self.dcpmap[dc_id].name, dc_id))

            # make sure to increment dc_id for the next one
            dc_id += 1

	logging.info("all {} processes started".format(dc_id))

    def _loop(self):
        # if no models are loaded, the loop is simpler
        if self.inq is None:
            while True and not self._should_stop():
                sleep(10)
            return

        # we have models and may need to process tasks
        while True and not self._should_stop():
            try:
                # get a task, block for 10 seconds
                task = self.inq.get(block=True, timeout=10)
            except Empty:
                # queue is empty and a timeout occurred before an item was added
                # check for stopage and try again
                continue

            dc_id, command, features = task

            if dc_id not in self.dcqmap:
                logging.warning("we don't have anywhere to send prediction for dc {}".format(dc_id))
                continue

            outq = self.dcqmap[dc_id]

            if command == 'purpose':
                is_rend_purp, _ = self.purpose_model.predict(features)
                outq.put([is_rend_purp])

            elif command == 'position':
                is_cgm_pos, _ =  self.position_model.predict(features)
                outq.put([is_cgm_pos])

            elif command == 'webpage':
                is_fb_site, _ = self.webpage_model.predict(features)
                outq.put([is_fb_site])

            else:
                logging.warning("got unrecognized command '{}' from dc {}".format(command, dc_id))

	    self.num_tasks_processed += 1

    def _should_stop(self):
        '''return true if we should stop processing events, cleanup, and exit'''

        # if this is the first time we are called, initialize
        if self.last_check_should_stop_time is None:
            self.last_check_should_stop_time = time()
            return False

        # only check process state every 60 seconds
        if time() - self.last_check_should_stop_time < 60.0:
            return False
        self.last_check_should_stop_time = time()

        num_alive = 0
        for dc_id in self.dcpmap:
            proc = self.dcpmap[dc_id]
            if proc.is_alive():
                num_alive += 1

        logging.info("{}/{} dc processes alive, {} tasks processed".format(num_alive,
            len(self.dcpmap), self.num_tasks_processed))

        if num_alive == 0:
            return True
        else:
            return False

    def _cleanup(self):
        logging.info("joining child data collector processes now")

        for dc_id in self.dcpmap:
            proc = self.dcpmap[dc_id]
            logging.info("attempting to join proc {} id {}".format(proc.name, dc_id))
            proc.join(5) # only wait 5 seconds

        logging.info("the machine learning data collector runner has completed")
