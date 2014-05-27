# Copyright 2014 OpenStack Foundation
# Copyright 2014 Tesora, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

import abc
from trove.guestagent.strategy import Strategy


class Replication(Strategy):
    """Base class for Replication Strategy implementation """
    __strategy_type__ = 'replication'
    __strategy_ns__ = 'trove.guestagent.strategies.replication'

    def __init__(self, context):
        self.context = context
        super(Replication, self).__init__()

    @abc.abstractmethod
    def get_master_ref(self, master_config):
        """Get reference to master site for replication strategy"""

    @abc.abstractmethod
    def snapshot_for_replication(self, mysql_service, location, master_config):
        """Capture snapshot of master db"""

    @abc.abstractmethod
    def enable_as_master(self, mysql_service, master_config):
        """Configure underlying database to act as master for replication"""

    @abc.abstractmethod
    def enable_as_slave(self, mysql_service, snapshot):
        """Configure underlying database as a slave of the given master"""

    @abc.abstractmethod
    def detach_slave(self, mysql_service):
        """Turn off replication on a slave site"""

    @abc.abstractmethod
    def demote_master(self, mysql_service):
        """Turn off replication on a master site"""