class GlobalStatistics:
    def __init__(self, cases, deaths, recoveries, today_cases, today_deaths, today_recoveries, total_critical,
                active, tests, cases_per_million, deaths_per_million, tests_per_million, active_per_million,
                recoveries_per_million, critical_per_million, one_case_per_people, one_death_per_people, one_test_per_people, 
                population, infected_countries, updated):
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries
        self.today_cases = today_cases
        self.today_deaths = today_deaths
        self.today_recoveries = today_recoveries
        self.critical = total_critical
        self.active = active
        self.tests = tests
        self.cases_per_million = cases_per_million
        self.deaths_per_million = deaths_per_million
        self.tests_per_million = tests_per_million
        self.active_per_million = active_per_million
        self.recoveries_per_million = recoveries_per_million
        self.critical_per_million = critical_per_million
        self.population = population
        self.infected_countries = infected_countries
        self.updated = updated


class CountryInfo:
    def __init__(self, _id, iso2, iso3, _lat, _long, flag):
        self.id = _id
        self.iso2 = iso2
        self.iso3 = iso3
        self.latitude = _lat
        self.longitude = _long
        self.flag = flag


class CountryStatistics:
    def __init__(self, info, name, cases, deaths, recoveries, today_cases, today_deaths, today_recoveries, critical,
                active, tests, cases_per_million, deaths_per_million, tests_per_million, recoveries_per_million,
                critical_per_million, active_per_million, one_case_per_people, one_death_per_people, one_test_per_people,
                continent, population, updated):
        self.info = info
        self.name = name
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries
        self.today_cases = today_cases
        self.today_deaths = today_deaths
        self.today_recoveries = today_recoveries
        self.critical = critical
        self.active = active
        self.tests = tests
        self.cases_per_million = cases_per_million
        self.deaths_per_million = deaths_per_million
        self.tests_per_million = tests_per_million
        self.recoveries_per_million = recoveries_per_million
        self.critical_per_million = critical_per_million
        self.active_per_million = active_per_million
        self.one_case_per_people = one_case_per_people
        self.one_death_per_people = one_death_per_people
        self.one_test_per_people = one_test_per_people
        self.continent = continent
        self.population = population
        self.updated = updated


class StateStatistics:
    def __init__(self, name, cases, deaths, today_cases, today_deaths, active, tests, cases_per_million, deaths_per_million, tests_per_million):
        self.name = name
        self.cases = cases
        self.deaths = deaths
        self.today_cases = today_cases
        self.today_deaths = today_deaths
        self.active = active
        self.tests = tests
        self.cases_per_million = cases_per_million
        self.deaths_per_million = deaths_per_million
        self.tests_per_million = tests_per_million


class HistoryEntry:
    def __init__(self, date, value):
        self.date = date
        self.value = value


class HistoricalStatistics:
    def __init__(self, name, case_history, death_history, recovery_history, province):
        self.name = name
        self.case_history = case_history
        self.death_history = death_history
        self.recovery_history = recovery_history
        self.province = province or None

    
class JhuCsseStatistics:
    def __init__(self, country, province, county, updated, confirmed_cases, deaths, recoveries, _lat, _long):
        self.country_name = country
        self.province_name = province
        self.county_name = county
        self.updated = updated
        self.confirmed_cases = confirmed_cases
        self.deaths = deaths
        self.recoveries = recoveries
        self.latitude = _lat
        self.longitude = _long


class ContinentStatistics:
    def __init__(self, name, countries, cases, deaths, recoveries, critical, active, tests, today_cases,
                 today_deaths, today_recoveries, cases_per_million, deaths_per_million, tests_per_million,
                 active_per_million, recoveries_per_million, critical_per_million, population, updated):
        self.name = name
        self.countries = countries
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries
        self.critical = critical
        self.active = active
        self.tests = tests
        self.today_cases = today_cases
        self.today_deaths = today_deaths
        self.today_recoveries = today_recoveries
        self.cases_per_million = cases_per_million
        self.deaths_per_million = deaths_per_million
        self.tests_per_million = tests_per_million
        self.active_per_million = active_per_million
        self.recoveries_per_million = recoveries_per_million
        self.critical = critical_per_million
        self.population = population
        self.updated = updated


class NewYorkTimesUsaStatistics:
    def __init__(self, date, cases, deaths):
        self.date = date
        self.cases = cases
        self.deaths = deaths


class NewYorkTimesStateStatistics:
    def __init__(self, date, state, fips, cases, deaths):
        self.date = date
        self.state = state
        self.fips = int(fips) if fips else None
        self.cases = cases
        self.deaths = deaths


class NewYorkTimesCountyStatistics:
    def __init__(self, date, county, state, fips, cases, deaths):
        self.date = date
        self.county = county
        self.state = state
        self.fips = int(fips) if fips else None
        self.cases = cases
        self.deaths = deaths


class AppleSubregions:
    def __init__(self, country, subregions):
        self.country = country
        self.subregions = subregions


class AppleSubregionStatistics:
    def __init__(self, subregion, statistics):
        self.subregion = subregion
        self.statistics = statistics


class AppleMobilityData:
    def __init__(self, name, _type, date, driving, transit, walking):
        self.name = name
        self.type = _type
        self.date = date
        self.driving = driving
        self.transit = transit
        self.walking = walking