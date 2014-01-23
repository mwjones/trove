# Copyright (c) 2013 Rackspace
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

from trove.common import cfg
from trove.guestagent import dbaas
from trove.guestagent import volume
from trove.guestagent.datastore.redis.service import RedisAppStatus
from trove.guestagent.datastore.redis.service import RedisApp
from trove.guestagent.datastore.redis import system
from trove.openstack.common import log as logging
from trove.openstack.common.gettextutils import _
from trove.openstack.common import periodic_task


LOG = logging.getLogger(__name__)
CONF = cfg.CONF


class Manager(periodic_task.PeriodicTasks):
    """
    This is the Redis manager class. It is dynamically loaded
    based off of the service_type of the trove instance
    """

    @periodic_task.periodic_task(ticks_between_runs=3)
    def update_status(self, context):
        """
        Updates the redis trove instance. It is decorated with
        perodic task so it is automatically called every 3 ticks.
        """
        RedisAppStatus.get().update()

    def change_passwords(self, context, users):
        """
        Changes the redis instance password,
        it is currently not not implemented.
        """
        raise NotImplemented()

    def reset_configuration(self, context, configuration):
        """
        Resets to the default configuration,
        currently this does nothing.
        """
        app = RedisApp(RedisAppStatus.get())
        app.reset_configuration(configuration)

    def _perform_restore(self, backup_info, context, restore_location, app):
        """
        Perform a restore on this instance,
        currently it is not implemented.
        """
        raise NotImplemented()

    def prepare(self, context, packages, databases, memory_mb, users,
                device_path=None, mount_point=None, backup_info=None,
                config_contents=None, root_password=None):
        """
        This is called when the trove instance first comes online.
        It is the first rpc message passed from the task manager.
        prepare handles all the base configuration of the redis instance.
        """
        app = RedisApp(RedisAppStatus.get())
        RedisAppStatus.get().begin_install()
        if device_path:
            device = volume.VolumeDevice(device_path)
            device.format()
            device.mount(system.REDIS_BASE_DIR)
            LOG.debug(_('Mounted the volume.'))
        app.install_if_needed(packages)
        LOG.info(_('Securing redis now.'))
        app.write_config(config_contents)
        app.complete_install_or_restart()
        LOG.info(_('"prepare" redis call has finished.'))

    def restart(self, context):
        """
        Restart this redis instance.
        This method is called when the guest agent
        gets a restart message from the taskmanager.
        """
        app = RedisApp(RedisAppStatus.get())
        app.restart()

    def start_db_with_conf_changes(self, context, config_contents):
        """
        Start this redis instance with new conf changes.
        Right now this does nothing.
        """
        raise NotImplemented()

    def stop_db(self, context, do_not_start_on_reboot=False):
        """
        Stop this redis instance.
        This method is called when the guest agent
        gets a stop message from the taskmanager.
        """
        app = RedisApp(RedisAppStatus.get())
        app.stop_db(do_not_start_on_reboot=do_not_start_on_reboot)

    def get_filesystem_stats(self, context, fs_path):
        """
        Gets file system stats from the provided fs_path.
        """
        return dbaas.get_filesystem_volume_stats(fs_path)

    def create_backup(self, context, backup_info):
        """
        This will eventually create a backup. Right now
        it does nothing.
        """
        raise NotImplemented()
