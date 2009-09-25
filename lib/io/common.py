# MolMod is a collection of molecular modelling tools for python.
# Copyright (C) 2007 - 2008 Toon Verstraelen <Toon.Verstraelen@UGent.be>
#
# This file is part of MolMod.
#
# MolMod is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# MolMod is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --
"""Common functionality used by the molmod.io package"""

__all__ = ["slice_match", "FileFormatError", "SlicedReader"]


def slice_match(sub, counter):
    """Efficiently test if counter is in xrange(*sub)

       Arguments:
         sub  --  a slice object
         counter  -- an integer

       The function returns True if the counter is in
       xrange(sub.start, sub.stop, sub.step).
    """

    if sub.start is not None and counter < sub.start:
        return False
    if sub.stop is not None and counter >= sub.stop:
        raise StopIteration
    if sub.step is not None:
        if sub.start is None:
            if counter % sub.step != 0:
                return False
        else:
            if (counter - sub.start) % sub.step != 0:
                return False
    return True


class FileFormatError(Exception):
    """Is raised when unexpected data is encountered while reading a file"""
    pass


class SlicedReader(object):
    """Base class for readers that can read a slice of all the frames"""

    def __init__(self, f, sub=slice(None)):
        """Initialize a SliceReader instance

           Arguments:
             f  --  a filename or a file-like object
             sub  --  a slice indicating which frames to read/skip

        """
        if isinstance(f, file):
            self._auto_close = False
            self._f = f
        else:
            self._auto_close = True
            self._f = file(f)
        self._sub = sub
        self._counter = 0

    def __del__(self):
        """Clean up the open file"""
        if self._auto_close:
            self._f.close()

    def _read_frame(self):
        """Read a single frame from the trajectory"""
        raise NotImplementedError

    def _skip_frame(self):
        """Skip a single frame from the trajectory"""
        raise NotImplementedError

    def __iter__(self):
        return self

    def next(self):
        """Read the next frame from the XYZ trajectory file

           This method is part of the iterator protocol
        """
        if self._first is not None:
            tmp = self._first
            self._first = None
            result = tmp
        else:
            result = self._read()[1:]
        if result is None:
            raise StopIteration
        return result

    def next(self):
        """Get the next frame from the file, taking into account the slice

           This method is part of the iterator protocol.
        """
        # skip frames as requested
        while not slice_match(self._sub, self._counter):
            self._counter += 1
            self._skip_frame()

        result = self._read_frame()
        self._counter += 1
        return result


