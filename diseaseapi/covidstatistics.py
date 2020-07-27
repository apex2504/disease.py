class Today:
    def __init__(self, cases, deaths, recoveries):
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries


class PerMillion:
    def __init__(self, cases, deaths, tests, active, recoveries, critical):
        self.cases = cases
        self.deaths = deaths
        self.tests = tests
        self.active = active
        self.recoveries = recoveries
        self.critical = critical


class PerPeople:
    def __init__(self, case, death, test):
        self.case = case
        self.death = death
        self.test = test


class Global:
    def __init__(self, cases, deaths, recoveries, today, total_critical, active, tests, per_million,
                per_people, population, affected_countries, updated):
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries
        self.today = today
        self.critical = total_critical
        self.active = active
        self.tests = tests
        self.per_million = per_million
        self.per_people = per_people
        self.population = population
        self.affected_countries = affected_countries
        self.updated = updated


class CountryInfo:
    def __init__(self, _id, iso2, iso3, _lat, _long, flag):
        self.id = _id
        self.iso2 = iso2
        self.iso3 = iso3
        self.latitude = _lat
        self.longitude = _long
        self.flag = flag


class Country:
    def __init__(self, info, name, cases, deaths, recoveries, today, critical, active, tests,
                per_million, per_people, continent, population, updated):
        self.info = info
        self.name = name
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries
        self.today = today
        self.critical = critical
        self.active = active
        self.tests = tests
        self.per_million = per_million
        self.per_people = per_people
        self.continent = continent
        self.population = population
        self.updated = updated


class StateToday:
    def __init__(self, cases, deaths):
        self.cases = cases
        self.deaths = deaths


class StatePerMillion:
    def __init__(self, cases, deaths, tests):
        self.cases = cases
        self.deaths = deaths
        self.tests = tests


class State:
    def __init__(self, name, cases, deaths, today, active, tests, per_million):
        self.name = name
        self.cases = cases
        self.deaths = deaths
        self.today = today
        self.active = active
        self.tests = tests
        self.per_million = per_million


class HistoryEntry:
    def __init__(self, date, value):
        self.date = date
        self.value = value


class History:
    def __init__(self, cases, deaths, recoveries):
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries


class Historical:
    def __init__(self, name, province, history):
        self.name = name
        self.province = province or None
        self.history = history

    
class JhuCsse:
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


class Continent:
    def __init__(self, name, countries, cases, deaths, recoveries, critical, active, tests, today,
                per_million, population, updated):
        self.name = name
        self.countries = countries
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries
        self.critical = critical
        self.active = active
        self.tests = tests
        self.today = today
        self.per_million = per_million
        self.population = population
        self.updated = updated


class NewYorkTimesUsa:
    def __init__(self, date, cases, deaths):
        self.date = date
        self.cases = cases
        self.deaths = deaths


class NewYorkTimesState:
    def __init__(self, date, state, fips, cases, deaths):
        self.date = date
        self.state = state
        self.fips = int(fips) if fips else None
        self.cases = cases
        self.deaths = deaths


class NewYorkTimesCounty:
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


class AppleSubregion:
    def __init__(self, subregion, statistics):
        self.subregion = subregion
        self.statistics = statistics


class Mobility:
    def __init__(self, name, _type, date, driving, transit, walking):
        self.name = name
        self.type = _type
        self.date = date
        self.driving = driving
        self.transit = transit
        self.walking = walking


class Vaccine:
    def __init__(self, candidate, sponsors, details, phase, institutions, funding):
        self.candidate = candidate
        self.sponsors = sponsors
        self.details = details
        self.phase = phase
        self.institutions = institutions
        self.funding = funding


class Vaccines:
    def __init__(self, source, vaccines):
        self.source = source
        self.vaccines = vaccines