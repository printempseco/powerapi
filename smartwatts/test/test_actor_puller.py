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
Module test_actor_puller
"""

import zmq
from smartwatts.puller import ActorPuller
from smartwatts.database import MongoDB
from smartwatts.filter import HWPCFilter
from smartwatts.report import HWPCReport
from smartwatts.report_model import HWPCModel
from smartwatts.test import MessageInterceptor

#########################################
# Initialization functions
#########################################


def get_hwpc_mongodb(collection):
    """ Return a MongoDB object for hwpc report """
    return MongoDB(HWPCModel(), 'localhost', 27017, 'test_puller', collection)


def get_hwpc_filter(dispatch):
    """ Return hwpcfilter with rule for the param dispatch """
    hwpc_filter = HWPCFilter()
    hwpc_filter.filter(lambda msg: True, dispatch)
    return hwpc_filter

#########################################


class TestActorPuller:
    """ TestActorPuller class """

    def test_basic_db(self):
        """ Test get 10 simple HWPCReport """
        context = zmq.Context()
        interceptor = MessageInterceptor(context)
        puller = ActorPuller("puller_mongo", get_hwpc_mongodb('test_puller1'),
                             get_hwpc_filter(interceptor), 10)
        puller.start()
        puller.connect(context)

        # Get the 10 HWPCReport
        for _ in range(10):
            report = interceptor.receive(100)
            assert isinstance(report, HWPCReport)

        # Get one more
        report = interceptor.receive(100)
        assert report is None

        puller.kill()