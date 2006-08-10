# MolMod is a collection of molecular modelling tools for python.
# Copyright (C) 2005 Toon Verstraelen
#
# This file is part of MolMod.
#
# MolMod is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# --


from binning import IntraAnalyseNeighboringObjects

import numpy


__all__ = ["Environment", "calculate_environments"]


class Environment(object):
    def __init__(self, positioned):
        self.__dict__.update(positioned.__dict__)
        deltas = []
        distances = []


def calculate_environments(sparse_binned_objects, radius, unit_cell=None):
    # this is a function that will extract the environment of each object
    def delta_distance(positioned1, positioned2):
        delta = positioned2.vector - positioned1.vector
        if unit_cell is not None:
            delta = unit_cell.shortest_vector(delta)
        distance = numpy.linalg.norm(delta)

        if distance <= radius:
            return delta, distance

    environments = {}
    def add_to_environments(positioned_a, positioned_b, delta, distance):
        environment_a = environments.get(positioned_a.id)
        if environment_a is None:
            environment_a = Environment(positioned_a)
            environment_a.deltas = []
            environment_a.distances = []
            environment_a.neighbors = []
            environment_a.reverse_neighbors = {}
            environments[positioned_a.id] = environment_a
        environment_a.deltas.append(delta)
        environment_a.distances.append(distance)
        environment_a.neighbors.append(positioned_b.id)
        environment_a.reverse_neighbors[positioned_b.id] = len(environment_a.reverse_neighbors)

    # now compare 'all' distances
    for (positioned1, positioned2), (delta, distance) in IntraAnalyseNeighboringObjects(sparse_binned_objects, delta_distance)(unit_cell):
        add_to_environments(positioned1, positioned2,  delta, distance)
        add_to_environments(positioned2, positioned1, -delta, distance)

    # At this time we have for each object a set of vectors that
    # point to other objects within the range of radius. Now we will
    # calculate some aditional information
    for environment in environments.itervalues():
        n = len(environment.deltas)
        environment.deltas = numpy.array(environment.deltas)
        environment.distances = numpy.array(environment.distances)
        environment.directions = (environment.deltas.transpose() / (environment.distances + (environment.distances == 0.0))).transpose()

    return environments