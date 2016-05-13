'''backend_python_logging.py - logging backend using Python logging

Note: this is intended only for informal debugging.
'''

import logging
import rh_logger.api
import sys


class BLPLogger(rh_logger.api.Logger):
    def __init__(self, name, args):
        self.logger = logging.getLogger(name)
        self.args = args

    def start_process(self, msg):
        '''Report the start of a process

        :param msg: an introductory message for the process
        '''
        self.logger.info("Starting process: %s (%s)" %
                         (msg, repr(self.args)))

    def end_process(self, msg, exit_code):
        '''Report the end of a process

        :param msg: an informative message about why the process ended
        :param exit_code: one of the :py:class: `ExitCode` enumerations
        '''
        self.logger.info("Ending process: %s, exit code = %s" %
                         (msg, exit_code.name))

    def report_metric(self, name, metric, subcontext=None):
        '''Report a metric such as accuracy or execution time

        :param name: name of the metric, e.g. "Rand score"
        :param metric: the value
        :param subcontext: an optional sequence of objects identifying a
        subcontext for the metric such as a tile of the MFOV being processed.
        '''
        if subcontext is None:
            self.logger.info("Metric %s=%s" %
                             (name, str(metric)))
        else:
            self.logger.info("Metric %s=%s (%s)" %
                             (name, str(metric), subcontext))

    def report_event(self, event, context=None):
        '''Report an event

        :param event: the name of the event, for instance, "Frobbing complete"
        :param context: a subcontext such as "MFOV: 5, Tile: 3"
        '''
        if context is None:
            self.logger.info(event)
        else:
            self.logger.info("%s (%s)" % (event, repr(context)))

    def report_exception(self, exception=None, msg=None):
        '''Report an exception

        :param exception: the :py:class: `Exception` that was thrown. Default
        is the one reported by sys.exc_info()
        :param msg: an informative message
        '''
        if exception is None:
            if msg is None:
                msg = str(sys.exc_value)
            self.logger.exception(msg, exc_info=1)
        else:
            if msg is None:
                msg = str(exception)
            self.logger.error(msg)


def get_logger(name, args):
    '''Get the default rh_logging logger'''
    return BLPLogger(name, args)