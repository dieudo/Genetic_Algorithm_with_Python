import random
class GA(object):
    def __init__(self, Genes):
        self.Genes = Genes
        pass

    def run(self):
        POP = self.Genes.initial()
        while True:
            fitPOP = [(self.Genes.Fitness(ch),  ch) for ch in POP]
            if self.Genes.Check(fitPOP): break
            POP = self.next(fitPOP)
            pass
        return POP

    def next(self, fits):
        generateParent = self.Genes.Parent(fits)
        size = len(fits)
        nexts = []
        while len(nexts) < size:
            Parent = next(generateParent)
            cross = random.random() < self.Genes.crossoverProba()
            children = self.Genes.crossover(Parent) if cross else Parent
            for ch in children:
                mutate = random.random() < self.Genes.mutationProba()
                nexts.append(self.Genes.mutation(ch) if mutate else ch)
                pass
            pass
        return nexts[0:size]
    pass

class functionGenes(object):
    def crossoverProba(self):#return crossover rate 
        return 1.0

    def mutationProba(self):
        return 0.0

    def initial(self):
        return []

    def Fitness(self, chromosome):
        return len(chromosome)

    def Check(self, fitPOP):#stop run if returns true,list of fit populations
        return False

    def Parent(self, fitPOP):
        gen = iter(sorted(fitPOP))
        while True:
            f1, ch1 = next(gen)
            f2, ch2 = next(gen)
            yield (ch1, ch2)
            pass
        return

    def crossover(self, Parent):
        return Parent

    def mutation(self, chromosome):
        return chromosome
    pass

if __name__ == "__main__":

    class predictText(functionGenes):
        def __init__(self, Text,
                     limit=eval(input("Enter the Maximum number of Generations\n ")), size=eval(input("The maximum length of characters?\n")),
                     prob_crossover=eval(input("Enter your probability of crossover\n")), prob_mutation=eval(input("Enter your probability of mutation\n"))):
            self.optimalText = self.GenoToPheno(Text)
            self.counter = 0

            self.limit = limit
            self.size = size
            self.prob_crossover = prob_crossover
            self.prob_mutation = prob_mutation
            pass

        def crossoverProba(self):
            return self.prob_crossover

        def mutationProba(self):
            return self.prob_mutation

        def initial(self):
            return [self.randomChromosome() for j in range(self.size)]

        def Fitness(self, chromo):
            return -sum(abs(c - t) for c, t in zip(chromo, self.optimalText))

        def Check(self, fitPOP):
            self.counter += 1
            if self.counter % 10 == 0:
                best_match = list(sorted(fitPOP))[-1][1]
                fits = [f for f, ch in fitPOP]
                best = max(fits)
                worst = min(fits)
                ave = sum(fits) / len(fits)
                print(
                    "[G %3d] Fitness=(Best=%4d,Avg= %4d, Worst=%4d): %r" %
                    (self.counter, best, ave, worst,
                     self.PhenoToGeno(best_match)))
                pass
            return self.counter >= self.limit

        def Parent(self, fitPOP):
            while True:
                Parent1 = self.Compete(fitPOP)
                Parent2 = self.Compete(fitPOP)
                yield (Parent1, Parent2)
                pass
            pass

        def crossover(self, Parent):
            Parent1, Parent2 = Parent
            index1 = random.randint(1, len(self.optimalText) - 2)
            index2 = random.randint(1, len(self.optimalText) - 2)
            if index1 > index2: index1, index2 = index2, index1
            child1 = Parent1[:index1] + Parent2[index1:index2] + Parent1[index2:]
            child2 = Parent2[:index1] + Parent1[index1:index2] + Parent2[index2:]
            return (child1, child2)

        def mutation(self, chromosome):
            index = random.randint(0, len(self.optimalText) - 1)
            vary = random.randint(-5, 5)
            mutated = list(chromosome)
            mutated[index] += vary
            return mutated

        def Compete(self, fitPOP):
            Firstf, First = self.randomSelection(fitPOP)
            Secondf, Second = self.randomSelection(fitPOP)
            return First if Firstf > Secondf else Second

        def randomSelection(self, fitPOP):
            return fitPOP[random.randint(0, len(fitPOP)-1)]

        def GenoToPheno(self, text):
            return [ord(ch) for ch in text]
        def PhenoToGeno(self, chromo):
            return "".join(chr(max(1, min(ch, 255))) for ch in chromo)

        def randomChromosome(self):
            return [random.randint(1, 255) for i in range(len(self.optimalText))]
        pass

    GA(predictText(input("Enter your words here\n"))).run()
    pass
