# Path Check
#
# Authors:
# Taz Wake (t.wake@halkynconsulting.co.uk)
#
# This file is part of Volatility.
#
# Volatility is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Volatility is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Volatility.  If not, see <http://www.gnu.org/licenses/>.
#

import volatility.win32 as win32
import volatility.utils as utils
import volatility.plugins.common as common

from volatility.renderers import TreeGrid

class PathCheck(common.AbstractWindowsCommand):
    '''Checks image paths to look for unusual start locations'''

    def calculate(self):
        addr_space = utils.load_as(self._config)
        tasks = win32.tasks.pslist(addr_space)

        return tasks

    def generator(self, data):

        for task in data:
            response = ""
            temp = "temp"
            user = "user"
            dl ="download"
            imgPath = str(task.Peb.ProcessParameters.ImagePathName)
            if temp.lower() in imgPath.lower():
                response = "Possible Temp location"
                yield (0, [
                           str(task.UniqueProcessId),
                           str(task.ImageFileName),
                           str(response),
                           str(imgPath),
                       ])
            if user.lower() in imgPath.lower():
                response = "Possible User location"
                yield (0, [
                           str(task.UniqueProcessId),
                           str(task.ImageFileName),
                           str(response),
                           str(imgPath),
                       ])
            if dl.lower() in imgPath.lower():
                response = "Possible Download location"
                yield (0, [
                           str(task.UniqueProcessId),
                           str(task.ImageFileName),
                           str(response),
                           str(imgPath),
                       ])
                
    def unified_output(self, data):
        tree = [
               ("PID", str),
               ("Process", str),
               ("Status", str),
               ("Path", str),
               ]

        return TreeGrid(tree, self.generator(data))
