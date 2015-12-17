"""
    This file is part of GALE,
    Copyright Joe Krall, 2014.

    GALE is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GALE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with GALE.  If not, see <http://www.gnu.org/licenses/>.
"""

from Fastmap.Slurp import *
from Fastmap.Moo import *
from jmoo_individual import *


def galeWHERE(problem, population, configuration, values_to_be_passed):
    "The Core method behind GALE"

    # Compile population into table form used by WHERE
    t = slurp([[x for x in row.decisionValues] + ["?" for y in problem.objectives] for row in population],
              problem.buildHeader().split(","))

    # Initialize some parameters for WHERE
    The.allowDomination = True
    The.alpha = 1
    for i, row in enumerate(t.rows):
        row.evaluated = False

    # Run WHERE
    m = Moo(problem, t, len(t.rows), N=1).divide(minnie=rstop(t))

    # Organizing
    NDLeafs = m.nonPrunedLeaves()  # The surviving non-dominated leafs
    allLeafs = m.nonPrunedLeaves() + m.prunedLeaves()  # All of the leafs

    # After mutation: Check how many rows were actually evaluated
    numEval = 0
    for leaf in allLeafs:
        for row in leaf.table.rows:
            if row.evaluated:
                numEval += 1

    return NDLeafs, numEval


def furthest(individual, population):
    from euclidean_distance import euclidean_distance
    distances = sorted([[euclidean_distance(individual, pop), pop] for pop in population], key=lambda x: x[0], reverse=True)
    return distances[0][-1]


def projection(a, b, c):
    """
    Fastmap projection distance
    :param a: Distance from West
    :param b: Distance from East
    :param c: Distance between West and East
    :return: FastMap projection distance(float)
    """
    return (a**2 + c**2 - b**2) / (2*c+0.00001)


def fastmap(problem, true_population):
    """
    Fastmap function that projects all the points on the principal component
    :param problem: Instance of the problem
    :param population: Set of points in the cluster population
    :return:
    """

    def list_equality(lista, listb):
        for a, b in zip(lista, listb):
            if a != b: return False
        return True

    from random import choice
    from euclidean_distance import euclidean_distance

    decision_population = [pop.decisionValues for pop in true_population]
    one = choice(decision_population)
    west = furthest(one, decision_population)
    east = furthest(west, decision_population)

    west_indi = jmoo_individual(problem,west, None)
    east_indi = jmoo_individual(problem,east, None)
    west_indi.evaluate()
    east_indi.evaluate()


    # Score the poles
    n = len(problem.decisions)
    weights = []
    for obj in problem.objectives:
        # w is negative when we are maximizing that objective
        if obj.lismore:
            weights.append(+1)
        else:
            weights.append(-1)
    weightedWest = [c * w for c, w in zip(west_indi.fitness.fitness, weights)]
    weightedEast = [c * w for c, w in zip(east_indi.fitness.fitness, weights)]
    westLoss = loss(weightedWest, weightedEast, mins=[obj.low for obj in problem.objectives],
                    maxs=[obj.up for obj in problem.objectives])
    eastLoss = loss(weightedEast, weightedWest, mins=[obj.low for obj in problem.objectives],
                    maxs=[obj.up for obj in problem.objectives])

    # Determine better Pole
    if eastLoss < westLoss:
        SouthPole, NorthPole = east_indi, west_indi
    else:
        SouthPole, NorthPole = west_indi, east_indi


    east = SouthPole.decisionValues
    west = NorthPole.decisionValues

    c = euclidean_distance(east, west)
    tpopulation = []
    for one in decision_population:
        a = euclidean_distance(one, west)
        b = euclidean_distance(one, east)
        tpopulation.append([one, projection(a, b, c)])

    for tpop in tpopulation:
        for true_pop in true_population:
            if list_equality(tpop[0], true_pop.decisionValues):
                true_pop.x = tpop[-1]
    temp_list = sorted(true_population, key=lambda pop: pop.x)
    return true_population[:len(temp_list)/2]


def galeMutate(problem, leaves, configuration):
    #################
    # Mutation Phase
    #################

    # Keep track of evals
    numEval = 0

    for leaf in leaves:
        initial_length = len(leaf)
        reduced_population = fastmap(problem, leaf)
        regenerate_length = initial_length - len(reduced_population)
         generate more points



    return population, numEval


def galeRegen(problem, unusedslot, mutants, configuration):
    howMany = configuration["Universal"]["Population_Size"] - len(mutants)
    # Generate random individuals
    population = []
    for i in range(howMany):
        population.append(jmoo_individual(problem, problem.generateInput(), None))
    
    return mutants+population, 0
