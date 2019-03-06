#    Copyright 2019, A10 Networks
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

from oslo_config import cfg
from oslo_log import log as logging
import oslo_messaging as messaging

from octavia.api.drivers.exceptions import NotImplementedError
from octavia.api.drivers import provider_base as driver_base
from octavia.api.drivers import utils as driver_utils
from octavia.api.drivers import driver_lib
from octavia.common import constants as consts
from octavia.common import data_models
from octavia.common import utils
from octavia.db import api as db_apis
from octavia.db import repositories
from octavia.network import base as network_base
import threading

CONF = cfg.CONF
CONF.import_group('oslo_messaging', 'octavia.common.config')
LOG = logging.getLogger(__name__)


class A10ProviderDriver(driver_base.ProviderDriver):
    def __init__(self):
        super(A10ProviderDriver, self).__init__()
        topic = cfg.CONF.oslo_messaging.topic
        self.transport = messaging.get_rpc_transport(cfg.CONF)
        self.target = messaging.Target(
            namespace=consts.RPC_NAMESPACE_CONTROLLER_AGENT,
            topic=topic, version="1.0", fanout=False)
        self.client = messaging.RPCClient(self.transport, target=self.target)
        self.repositories = repositories.Repositories()
        self._octavia_driver_db = driver_lib.DriverLibrary()

    # Load Balancer
    def create_vip_port(self, loadbalancer_id, vip_dictionary, *args):
        """Creates a port for a load balancer VIP.

        If the driver supports creating VIP ports, the driver will create a
        VIP port and return the vip_dictionary populated with the vip_port_id.
        If the driver does not support port creation, the driver will raise
        a NotImplementedError.
        :param: loadbalancer_id (string): ID of loadbalancer.
        :param: vip_dictionary (dict): The VIP dictionary.
        :returns: VIP dictionary with vip_port_id.
        :raises DriverError: An unexpected error occurred in the driver.
        :raises NotImplementedError: The driver does not support creating
        VIP ports.
        """
        #import pdb; pdb.set_trace()
        raise NotImplementedError()

    def loadbalancer_create(self, loadbalancer):
        """Creates a new load balancer.

        :param loadbalancer (object): The load balancer object.
        :return: Nothing if the create request was accepted.
        :raises DriverError: An unexpected error occurred in the driver.
        :raises NotImplementedError: The driver does not support create.
        :raises UnsupportedOptionError: The driver does not
         support one of the configuration options.
         """
  
        errorString = "We are just started, dont expect much.."

        print("imagine we have completed ACOS calls here")

        # setting up status ACTIVE/ERROR based on ACOS call
        status = {
                 'loadbalancers': [{"id": loadbalancer.loadbalancer_id,
                 "provisioning_status": consts.ACTIVE }]}
        print(status)
        # Using Threads to update DB
        print("updating the database using new thread")
        DBHelper(status)
        #self.updateStatus(status)
        #raise NotImplementedError(user_fault_string=errorString)


    def updateStatus(self, status):
        self._octavia_driver_db.update_loadbalancer_status(status)

class DBHelper():
    def __init__(self, status):
        self.status = status
        self._octavia_driver_db = driver_lib.DriverLibrary()
        thread = threading.Thread(target=self.updateStatus, args=())
        thread.daemon = True
        thread.start() 

    def updateStatus(self):
        self._octavia_driver_db.update_loadbalancer_status(self.status)

