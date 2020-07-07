class ILIPercent:
    def __init__(self, weighted, unweighted):
        self.weighted = weighted
        self.unweighted = unweighted

class ILINetData:
    def __init__(self, week, ages, total_ili, total_patients, 
                percentages):
        self.week = week
        self.ages = ages
        self.total_ili = total_ili
        self.total_patients = total_patients
        self.percentages = percentages


class ILINet:
    def __init__(self, updated, source, data):
        self.updated = updated
        self.source = source
        self.stats = data


class USCLPercent:
    def __init__(self, positive_a, positive_b, total):
        self.positive_a = positive_a
        self.positive_b = positive_b
        self.total = total


class USCLTotal:
    def __init__(self, a, b, tests):
        self.type_a = a
        self.type_b = b
        self.tests = tests

class USCLData:
    def __init__(self, week, totals, percentages):
        self.week = week
        self.totals = totals
        self.percentages = percentages


class USCL:
    def __init__(self, updated, source, data):
        self.updated = updated
        self.source = source
        self.stats = data


class TypeA:
    def __init__(self, h3n2v, h1n1, h3, unable_to_subtype, subtyping_not_performed):
        self.h3n2v = h3n2v
        self.h1n1 = h1n1
        self.h3 = h3
        self.unable_to_subtype = unable_to_subtype
        self.subtyping_not_performed = subtyping_not_performed


class USPHLData:
    def __init__(self, week, a, b, bvic, byam, total_tests):
        self.week = week
        self.type_a = a
        self.type_b = b
        self.bvic = bvic
        self.byam = byam
        self.total_tests = total_tests


class USPHL:
    def __init__(self, updated, source, data):
        self.updated = updated
        self.source = source
        self.stats = data