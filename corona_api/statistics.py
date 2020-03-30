class GlobalStatistics:
    def __init__(self, cases, deaths, recoveries, today_cases, today_deaths, total_critical, active, updated):
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries
        self.today_cases = today_cases
        self.today_deaths = today_deaths
        self.critical = total_critical
        self.active = active
        self.updated = updated


class CountryStatistics:
    def __init__(self, name, cases, deaths, recoveries, today_cases, today_deaths, critical, active, cases_per_million, deaths_per_million, updated, flag):
        self.name = name
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries
        self.today_cases = today_cases
        self.today_deaths = today_deaths
        self.critical = critical
        self.active = active
        self.cases_per_million = cases_per_million
        self.deaths_per_million = deaths_per_million
        self.updated = updated
        self.flag = flag


class StateStatistics:
    def __init__(self, name, cases, deaths, today_cases, today_deaths, active):
        self.name = name
        self.cases = cases
        self.deaths = deaths
        self.today_cases = today_cases
        self.today_deaths = today_deaths
        self.active = active


class HistoryEntry:
    def __init__(self, date, value):
        self.date = date
        self.value = value


class HistoricalStatistics:
    def __init__(self, name, case_history, death_history, recovery_history):
        self.name = name
        self.case_history = case_history
        self.death_history = death_history
        self.recovery_history = recovery_history