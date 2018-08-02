# Copyright 2018-present Samsung Electronics Co., Ltd. and other contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from jstest.common import console
from jstest.testrunner import utils as testrunner_utils
from jstest.testrunner.devices.device_base import RemoteDevice
from jstest.testrunner.devices.connections.serialcom import SerialConnection


class SerialDevice(RemoteDevice):
    '''
    Common super class for serial devices.
    '''
    def __init__(self, env, os, prompt):
        RemoteDevice.__init__(self, env, os)

        data = {
            'dev-id': env['info']['device_id'],
            'baud': env['info']['baud'],
            'timeout': env['info']['timeout'],
            'prompt': prompt
        }

        self.channel = SerialConnection(data)

    def check_args(self):
        '''
        Check that all the arguments are established.
        '''
        if not self.env['info']['device_id']:
            console.fail('Please use the --device-id to select the device.')

    def reset(self):
        '''
        Dummy method.
        '''
        pass

    def _prepare_command(self, testset, test):
        '''
        Prepare the command which will be executed.
        '''
        # Absolute path to the test file on the device.
        testfile = '/test/%s/%s' % (testset, test['name'])

        args = []
        if not self.env['info']['no_memstat']:
            args = ['--mem-stats']

        if self.device == 'artik053' and self.env['info']['coverage']:
            args.append('--start-debug-server')
            port = testrunner_utils.read_port_from_url(self.env['info']['coverage'])
            args.append('--debug-port %s' % port)

        command = {
            'iotjs': 'iotjs %s %s' % (' '.join(args), testfile),
            'jerryscript': 'jerry %s %s' % (testfile, ' '.join(args))
        }

        return command