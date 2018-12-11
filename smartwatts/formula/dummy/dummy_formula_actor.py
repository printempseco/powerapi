# Copyright (C) 2018  University of Lille
# Copyright (C) 2018  INRIA
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Module ActorTestFormula
"""
import time
from smartwatts.formula.formula_actor import FormulaActor
from smartwatts.message import UnknowMessageTypeException
from smartwatts.report import Report, PowerReport
from smartwatts.handler import AbstractHandler


class DummyHWPCReportHandler(AbstractHandler):
    """
    A test formula that simulate data processing
    """

    def __init__(self, actor_pusher):
        self.actor_pusher = actor_pusher

    def _process_report(self, report):
        """ Wait 1 seconde and return a power report containg 42

        Parameters:
            (smartwatts.report.Report): received report

        Return:
            (smartwatts.report.PowerReport): a power report containing
                                             comsumption estimation

        """

        time.sleep(1)
        result_msg = PowerReport(report.timestamp, report.sensor,
                                 report.target, {}, 42)
        return result_msg

    def handle(self, msg, state):
        """ process a report and send the result to the pusher actor

        Parameters:
            msg(smartwatts.report.Report) : received message
            state(smartwatts.actor.BasicState) : current actor state

        Return:
            state(smartwatts.actor.BasicState): new actor state

        Raise:
            UnknowMessageTypeException: if the *msg* is not a Report
        """
        if not isinstance(msg, Report):
            raise UnknowMessageTypeException(type(msg))

        result = self._process_report(msg)
        self.actor_pusher.send(result)
        return state


class DummyFormulaActor(FormulaActor):
    """
    ActorTestFormula class

    A test formula that simulate data processing by waiting 1s and send a
    power report containing 42
    """

    def __init__(self, name, actor_pusher, verbose=False):
        """
        Parameters:
            @pusher(smartwatts.pusher.ActorPusher): Pusher to whom this formula
                                                    must send its reports
        """
        FormulaActor.__init__(self, name, actor_pusher, verbose)

    def setup(self):
        """ Initialize Handler """
        FormulaActor.setup(self)
        self.handlers.append((Report,
                              DummyHWPCReportHandler(self.actor_pusher)))