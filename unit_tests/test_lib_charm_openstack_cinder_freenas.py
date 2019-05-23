# Copyright 2016 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import print_function

import charmhelpers

import charm.openstack.cinder_freenas as cinder_freenas

import charms_openstack.test_utils as test_utils


class TestCinderFreeNASCharm(test_utils.PatchHelper):

    def _patch_config_and_charm(self, config):
        self.patch_object(charmhelpers.core.hookenv, 'config')

        def cf(key=None):
            if key is not None:
                return config[key]
            return config

        self.config.side_effect = cf
        c = cinder_freenas.CinderFreeNASCharm()
        return c

    def test_cinder_base(self):
        charm = self._patch_config_and_charm({})
        self.assertEqual(charm.name, 'cinder_freenas')
        self.assertEqual(charm.version_package, 'python-cinder-freenas')
        self.assertEqual(charm.packages, ['python-cinder-freenas'])

    def test_cinder_configuration(self):
        charm = self._patch_config_and_charm({
            'volume-dd-blocksize': '1024',
            'nas-login': 'root',
            'nas-password': 'password',
            'nas-server-hostname': '192.168.0.1',
            'nas-volume-backend-name': 'iXsystems_FREENAS_Storage',
            'nas-iqn-prefix': 'iqn.2005-10.org.freenas.ctl',
            'nas-datastore-pool': 'vol1',
            'nas-vendor-name': 'iXsystems',
            'nas-storage-protocol': 'iscsi'})
        config = charm.cinder_configuration()  # noqa
        self.assertEqual(config, [
            ('iscsi_helper', 'tgtadm'),
            ('volume_dd_blocksize', '1024'),
            ('volume_driver', ('cinder.volume.drivers.ixsystems.iscsi.'
                               'FreeNASISCSIDriver')),
            ('ixsystems_login', 'root'),
            ('ixsystems_password', 'password'),
            ('ixsystems_server_hostname', '192.168.0.1'),
            ('ixsystems_volume_backend_name', 'iXsystems_FREENAS_Storage'),
            ('ixsystems_iqn_prefix', 'iqn.2005-10.org.freenas.ctl'),
            ('ixsystems_datastore_pool', 'vol1'),
            ('ixsystems_vendor_name', 'iXsystems'),
            ('ixsystems_storage_protocol', 'iscsi')])
