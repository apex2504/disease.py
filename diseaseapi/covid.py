from datetime import datetime, timezone
from typing import Union, List, Dict, Tuple
from .covidstatistics import *
from .exceptions import NotFound, BadSortParameter, BadYesterdayParameter, BadTwoDaysAgoParameter, BadAllowNoneParameter
from .covidendpoints import *


class Covid:
    """
    Handles interactions with the Open Disease API's COVID-19 data.
    """
    def __init__(self, api_url, request_client):
        self.api_url = api_url
        self.request_client = request_client


    def _check_sort(self, sort):
        if sort not in ['updated', 'country', 'countryInfo', 'cases', 'todayCases', 'deaths', 'todayDeaths', 'recovered',
                        'todayRecovered', 'active', 'critical', 'casesPerOneMillion', 'deathsPerOneMillion', 'tests',
                        'testsPerOneMillion', 'population', 'continent', 'oneCasePerPeople', 'oneDeathPerPeople',
                        'oneTestPerPeople', 'activePerOneMillion', 'recoveredPerOneMillion', 'criticalPerOneMillion']:
            raise BadSortParameter('Invalid sort parameter.')


    def _check_yesterday(self, value):
        if not isinstance(value, bool):
            raise BadYesterdayParameter('Value for yesterday should either be True or False.')


    def _check_two_days_ago(self, value):
        if not isinstance(value, bool):
            raise BadTwoDaysAgoParameter('Value for two_days_ago should either be True or False.')


    def _check_allow_none(self, value):
        if not isinstance(value, bool):
            raise BadAllowNoneParameter('Value for allow_none should either be True or False.')


    def _compile_today(self, data):
        return Today(
            data.get('todayCases'),
            data.get('todayDeaths'),
            data.get('todayRecovered')
        )


    def _compile_permillion(self, data):
        return PerMillion(
            data.get('casesPerOneMillion'),
            data.get('deathsPerOneMillion'),
            data.get('testsPerOneMillion'),
            data.get('activePerOneMillion'),
            data.get('recoveredPerOneMillion'),
            data.get('criticalPerOneMillion')
        )


    def _compile_perpeople(self, data):
        return PerPeople(
            data.get('oneCasePerPeople'),
            data.get('oneDeathPerPeople'),
            data.get('oneTestPerPeople')
        )


    def _compile_statetoday(self, data):
        return StateToday(
            data.get('todayCases'),
            data.get('todayDeaths')
        )


    def _compile_statepermillion(self, data):
        return StatePerMillion(
            data.get('casesPerOneMillion'),
            data.get('deathsPerOneMillion'),
            data.get('testsPerOneMillion')
        )


    def _compile_countryInfo(self, countryInfo):
        _id = countryInfo.get("_id")
        iso2 = countryInfo.get("iso2")
        iso3 = countryInfo.get("iso3")
        _lat = countryInfo.get("lat")
        _long = countryInfo.get("long")
        flag = countryInfo.get("flag")

        info = CountryInfo(
            _id,
            iso2,
            iso3,
            _lat,
            _long,
            flag
        )

        return info


    def _compile_country_data(self, country_stats):
        country_name = country_stats.get("country")
        total_country_cases = country_stats.get("cases", 0)
        total_country_deaths = country_stats.get("deaths", 0)
        total_country_recoveries = country_stats.get("recovered", 0)
        today = self._compile_today(country_stats)
        total_critical = country_stats.get("critical", 0)
        active = country_stats.get("active", 0)
        tests = country_stats.get("tests", 0)
        per_million = self._compile_permillion(country_stats)
        per_people = self._compile_perpeople(country_stats)
        continent = country_stats.get("continent")
        population = country_stats.get("population", 0)
        updated_epoch = country_stats.get("updated", 0)
        updated = datetime.utcfromtimestamp(updated_epoch/1000.0)

        countryInfo = country_stats["countryInfo"]

        info = self._compile_countryInfo(countryInfo)

        return Country(
            info,
            country_name,
            total_country_cases,
            total_country_deaths,
            total_country_recoveries,
            today,
            total_critical,
            active,
            tests,
            per_million,
            per_people,
            continent,
            population,
            updated
        )


    def _compile_state(self, state_dict):
        state_name = state_dict.get("state")
        total_state_cases = state_dict.get("cases", 0)
        total_state_deaths = state_dict.get("deaths", 0)
        today = self._compile_statetoday(state_dict)
        active = state_dict.get("active", 0)
        tests = state_dict.get("tests", 0)
        per_million = self._compile_statepermillion(state_dict)

        state_stats = State(
        state_name,
        total_state_cases,
        total_state_deaths,
        today,
        active,
        tests,
        per_million
        )

        return state_stats


    def _generate_history(self, historical_stats, is_county=False):
        case_history = []
        death_history = []
        recovery_history = [] if not is_county else None

        if not is_county:        
            country_name = historical_stats.get("country", "Global")
            province_name = historical_stats.get("province")


        else:
            country_name = historical_stats.get("province")
            province_name = historical_stats.get("county")

        if "timeline" not in historical_stats: #if country was 'all'
            d = historical_stats

        else:
            d = historical_stats["timeline"]

        for date in list(d["cases"].keys()): #pass on all historical data. let the client decide how much of it they want
            _d = datetime.strptime(date, "%m/%d/%y")
            case_history.append(HistoryEntry(_d, d["cases"][date]))
            death_history.append(HistoryEntry(_d, d["deaths"][date]))
            if not is_county:
                recovery_history.append(HistoryEntry(date, d["recovered"][date]))

        his = History(
            case_history,
            death_history,
            recovery_history
        )

        return Historical(
            country_name,
            province_name,
            his
        )


    def _compile_jhu_data(self, matching_county):
        country = matching_county.get("country") #will always be 'US'
        province = matching_county.get("province")
        county_name = matching_county.get("county")
        confirmed_cases = matching_county["stats"].get("confirmed")
        deaths = matching_county["stats"].get("deaths")
        recoveries = matching_county["stats"].get("recovered")
        _lat = float(matching_county["coordinates"].get("latitude")) if matching_county["coordinates"].get("latitude") else 0.0
        _long = float(matching_county["coordinates"].get("longitude")) if matching_county["coordinates"].get("longitude") else 0.0

        updated = datetime.strptime(matching_county.get('updatedAt'), '%Y-%m-%d %H:%M:%S')

        stat = JhuCsse(
                country,
                province,
                county_name,
                updated,
                confirmed_cases,
                deaths,
                recoveries,
                _lat,
                _long
                )

        return stat


    def _compile_continent(self, data):
        name = data.get('continent')
        countries = data.get('countries')
        cases = data.get("cases", 0)
        deaths = data.get("deaths", 0)
        recoveries = data.get("recovered", 0)
        today = self._compile_today(data)
        critical = data.get("critical", 0)
        updated_epoch = data.get("updated", 0)
        active = data.get("active", cases-deaths-recoveries)
        tests = data.get("tests", 0)
        per_million = self._compile_permillion(data)
        population = data.get("population", 0)
        updated = datetime.utcfromtimestamp(updated_epoch/1000.0)

        return Continent(
            name,
            countries,
            cases,
            deaths,
            recoveries,
            critical,
            active,
            tests,
            today,
            per_million,
            population,
            updated
        )    


    def _compile_state_list(self, data):
        return [self._compile_nyt_state(d) for d in data]


    def _compile_county_list(self, data):
        return [self._compile_nyt_county(d) for d in data]
    

    def _compile_nyt_state(self, data):
        date = data.get('date')
        state = data.get('state')
        fips = data.get('fips')
        cases = data.get('cases')
        deaths = data.get('deaths')

        if date:
            date = datetime.strptime(date, "%Y-%m-%d")

        return NewYorkTimesState(
            date,
            state,
            fips,
            cases,
            deaths
        )


    def _compile_nyt_county(self, data):
        date = data.get('date')
        county = data.get('county')
        state = data.get('state')
        fips = data.get('fips')
        cases = data.get('cases')
        deaths = data.get('deaths')

        if date:
            date = datetime.strptime(date, "%Y-%m-%d")

        return NewYorkTimesCounty(
            date,
            county,
            state,
            fips,
            cases,
            deaths
        )


    def _compile_apple_stats(self, data):
        name = data.get("subregion_and_city")
        _type = data.get("get_type")
        date = data.get("date")
        driving = data.get("driving")
        transit = data.get("transit")
        walking = data.get("walking")

        if date:
            date = datetime.strptime(date, "%Y-%m-%d")

        return Mobility(
            name,
            _type,
            date,
            driving,
            transit,
            walking
        )

    
    def _compile_vaccine(self, data):
        return Vaccine(
            data.get("candidate"),
            data.get("sponsors"),
            data.get("details"),
            data.get("trialPhase"),
            data.get("institutions"),
            data.get("funding")
        )

    
    def _compile_vaccines(self, data):
        source = data.get("source")

        return Vaccines(
            source,
            [self._compile_vaccine(vacc) for vacc in data["data"]]
        )


    def _compile_vax_tl(self, data):
        return [VaccineTimeline(datetime.strptime(date, '%m/%d/%y'), data[date]) for date in data]


    def _compile_vax_country(self, data):
        return VaccineCountry(data['country'], self._compile_vax_tl(data['timeline']))


######################################################################################


    async def all(self, **kwargs) -> Global:
        """
        Get the global stats for Coronavirus COVID-19
        """
        yesterday = kwargs.get('yesterday', False)
        two_days_ago = kwargs.get('two_days_ago', False)
        allow_none = kwargs.get('allow_none', False)

        endpoint = GLOBAL_DATA.format(self.api_url)

        if yesterday:
            self._check_yesterday(yesterday)

        if two_days_ago:
            self._check_two_days_ago(two_days_ago)

        if yesterday and two_days_ago:
            raise ValueError('yesterday and two_days_ago cannot both be True.')

        if allow_none:
            self._check_allow_none(allow_none)

        yesterday = str(yesterday).lower()
        two_days_ago = str(two_days_ago).lower()
        allow_none = str(allow_none).lower()
        params = {"yesterday": yesterday, "twoDaysAgo": two_days_ago, "allowNull": allow_none}

        global_data = await self.request_client.make_request(endpoint, params)

        cases = global_data.get("cases", 0)
        deaths = global_data.get("deaths", 0)
        recoveries = global_data.get("recovered", 0)
        today = self._compile_today(global_data)
        total_critical = global_data.get("critical", 0)
        updated_epoch = global_data.get("updated", 0)
        active = global_data.get("active", 0)
        tests = global_data.get("tests", 0)
        per_million = self._compile_permillion(global_data)
        per_people = self._compile_perpeople(global_data)
        population = global_data.get("population", 0)
        affected_countries = global_data.get("affectedCountries")
        updated = datetime.utcfromtimestamp(updated_epoch/1000.0)

        return Global(
            cases,
            deaths,
            recoveries,
            today,
            total_critical,
            active,
            tests,
            per_million,
            per_people,
            population,
            affected_countries,
            updated,
            )


    async def country(self, *countries, **kwargs) -> Union[Country, List[Country]]:
        """
        Get the data for more than one country, but not necessarily all of them.
        """
        yesterday = kwargs.get('yesterday', False)
        two_days_ago = kwargs.get('two_days_ago', False)
        allow_none = kwargs.get('allow_none', False)
        country_list = ','.join(map(str, countries))

        endpoint = COUNTRY_DATA.format(self.api_url, country_list)

        if yesterday:
            self._check_yesterday(yesterday)

        if two_days_ago:
            self._check_two_days_ago(two_days_ago)

        if yesterday and two_days_ago:
            raise ValueError('yesterday and two_days_ago cannot both be True.')

        if allow_none:
            self._check_allow_none(allow_none)

        yesterday = str(yesterday).lower()
        two_days_ago = str(two_days_ago).lower()
        allow_none = str(allow_none).lower()
        params = {"yesterday": yesterday, "twoDaysAgo": two_days_ago, "allowNull": allow_none}

        data = await self.request_client.make_request(endpoint, params)

        if isinstance(data, dict):
            return self._compile_country_data(data)

        return [self._compile_country_data(country) for country in data]


    async def all_countries(self, **kwargs) -> List[Country]:
        """
        Get the data for every affected country.
        """
        yesterday = kwargs.get('yesterday', False)
        two_days_ago = kwargs.get('two_days_ago', False)
        allow_none = kwargs.get('allow_none', False)
        sort = kwargs.get('sort', None)

        endpoint = ALL_COUNTRIES.format(self.api_url)
        params = None

        if yesterday:
            self._check_yesterday(yesterday)

        if two_days_ago:
            self._check_two_days_ago(two_days_ago)

        if yesterday and two_days_ago:
            raise ValueError('yesterday and two_days_ago cannot both be True.')

        if allow_none:
            self._check_allow_none(allow_none)

        yesterday = str(yesterday).lower()
        two_days_ago = str(two_days_ago).lower()
        allow_none = str(allow_none).lower()

        if sort:
            self._check_sort(sort)
            params = {"yesterday": yesterday, "twoDaysAgo": two_days_ago, "allowNull": allow_none, "sort": sort}

        else:
            params = {"yesterday": yesterday, "twoDaysAgo": two_days_ago, "allowNull": allow_none}
 
        all_countries = await self.request_client.make_request(endpoint, params)

        return [self._compile_country_data(c) for c in all_countries]


    async def all_states(self, **kwargs) -> List[State]:
        """
        Get the stats for all US states
        """
        yesterday = kwargs.get('yesterday', False)
        allow_none = kwargs.get('allow_none', False)
        sort = kwargs.get('sort', None)

        endpoint = ALL_STATES.format(self.api_url)
        params = None

        if yesterday:
            self._check_yesterday(yesterday)

        if allow_none:
            self._check_allow_none(allow_none)

        yesterday = str(yesterday).lower()
        allow_none = str(allow_none).lower()

        if sort:
            self._check_sort(sort)
            params = {"yesterday": yesterday, "allowNull": allow_none, "sort": sort}
        
        else:
            params = {"yesterday": yesterday, "allowNull": allow_none}

        state_info = await self.request_client.make_request(endpoint, params)

        return [self._compile_state(state) for state in state_info]

    
    async def state(self, *states, **kwargs) -> Union[State, List[State]]:
        """
        Get the stats for US States
        """
        yesterday = kwargs.get('yesterday', False)
        allow_none = kwargs.get('allow_none', False)
        state_list = ','.join(map(str, states))

        endpoint = SINGLE_STATE.format(self.api_url, state_list)

        if yesterday:
            self._check_yesterday(yesterday)

        if allow_none:
            self._check_allow_none(allow_none)
        
        yesterday = str(yesterday).lower()
        allow_none = str(allow_none).lower()
        params = {"yesterday": yesterday, "allowNull": allow_none}
            
        data = await self.request_client.make_request(endpoint, params)

        if isinstance(data, dict):
            return self._compile_state(data)
        
        return [self._compile_state(state) for state in data]


    async def country_history(self, country='all', last_days='all') -> Historical:
        """
        Get historical data for a specific country or globally.
        Defaults to 'all' in order to get global data. This can be overridden by the client.
        """
        endpoint = HISTORICAL_COUNTRY.format(self.api_url, country)
        params = {"lastdays": last_days}

        historical_stats = await self.request_client.make_request(endpoint, params)

        return self._generate_history(historical_stats)


    async def province_history(self, country, province, last_days='all') -> Historical:
        """
        Get the historical data for a province within a country.
        """
        endpoint = HISTORICAL_PROVINCE.format(self.api_url, country, province)
        params = {"lastdays": last_days}

        data = await self.request_client.make_request(endpoint, params)

        return self._generate_history(data)


    async def county_history(self, state, county, last_days='all') -> Historical:
        """
        Get the historical data for a county within a US state.
        """
        endpoint = STATE_COUNTY.format(self.api_url, state)
        params = {"lastdays": last_days}

        data = await self.request_client.make_request(endpoint, params)

        try:
            matching_county = next(place for place in data if place["province"].lower() == state.lower()
            and place["county"].lower() == county.lower())
        except StopIteration:
            raise NotFound('Nothing found for specified county.')

        return self._generate_history(matching_county, True)


    async def jhucsse(self) -> List[JhuCsse]:
        """
        Get data from the JHU CSSE.
        This includes province data for several countries
        """
        endpoint = JHU_CSSE.format(self.api_url)

        data = await self.request_client.make_request(endpoint)

        return [self._compile_jhu_data(cp) for cp in data]


    async def jhu_county(self, state, county) -> JhuCsse:
        """
        Get the data for a specific county within a US state.
        """
        endpoint = JHU_SINGLE_COUNTY.format(self.api_url, county)

        all_matching_counties = await self.request_client.make_request(endpoint)

        try:
            matching_county = next(place for place in all_matching_counties if place["province"].lower() == state.lower()
            and place["county"].lower() == county.lower())
        except StopIteration:
            raise NotFound('Nothing found for specified county.')

        return self._compile_jhu_data(matching_county)


    async def jhu_all_counties(self) -> List[JhuCsse]:
        """
        Get the data for every single county in the US provided by JHU.
        """
        endpoint = JHU_ALL_COUNTIES.format(self.api_url)

        data = await self.request_client.make_request(endpoint)

        return [self._compile_jhu_data(place) for place in data]


    async def all_continents(self, **kwargs) -> List[Continent]:
        """
        Get the statistics for world continents.
        """
        yesterday = kwargs.get('yesterday', False)
        two_days_ago = kwargs.get('two_days_ago', False)
        allow_none = kwargs.get('allow_none', False)
        sort = kwargs.get('sort', None)

        endpoint = ALL_CONTINENTS.format(self.api_url)
        params = None

        if yesterday:
            self._check_yesterday(yesterday)

        if two_days_ago:
            self._check_two_days_ago(two_days_ago)

        if yesterday and two_days_ago:
            raise ValueError('yesterday and two_days_ago cannot both be True.')

        if allow_none:
            self._check_allow_none(allow_none)

        yesterday = str(yesterday).lower()
        two_days_ago = str(two_days_ago).lower()
        allow_none = str(allow_none).lower()

        if sort:
            self._check_sort(sort)
            params = {"yesterday": yesterday, "twoDaysAgo": two_days_ago, "allowNull": allow_none, "sort": sort}

        else:
            params = {"yesterday": yesterday,"twoDaysAgo": two_days_ago, "allowNull": allow_none}

        data = await self.request_client.make_request(endpoint, params)

        return [self._compile_continent(c) for c in data]


    async def continent(self, continent, **kwargs) -> Continent:
        """
        Get the statistics for a single continent.
        """
        yesterday = kwargs.get('yesterday', False)
        two_days_ago = kwargs.get('two_days_ago', False)
        allow_none = kwargs.get('allow_none', False)

        endpoint = CONTINENT_DATA.format(self.api_url)
        params = None

        if yesterday:
            self._check_yesterday(yesterday)

        if two_days_ago:
            self._check_two_days_ago(two_days_ago)

        if yesterday and two_days_ago:
            raise ValueError('yesterday and two_days_ago cannot both be True.')

        yesterday = str(yesterday).lower()
        two_days_ago = str(two_days_ago).lower()
        allow_none = str(allow_none).lower()
        params = {"yesterday": yesterday, "allowNull": allow_none}

        data = await self.request_client.make_request(endpoint, params)

        return self._compile_continent(data)


    async def nyt(self) -> NewYorkTimesUsa:
        """
        Get historical data for the US from the New York Times
        """
        endpoint = NYT_USA.format(self.api_url)
        data = await self.request_client.make_request(endpoint)

        dates = []        

        for d in data:
            date = d.get('date')
            cases = d.get('cases')
            deaths = d.get('deaths')

            if date:
                date = datetime.strptime(date, "%Y-%m-%d")

            dates.append(
                NewYorkTimesUsa(
                    date,
                    cases,
                    deaths
                )
            )

        return dates


    async def nyt_states(self) -> List[NewYorkTimesState]:
        """
        Get the data for all states from New York Times
        """
        endpoint = NYT_ALL_STATES.format(self.api_url)
        data = await self.request_client.make_request(endpoint)

        states_list = self._compile_state_list(data)

        return states_list


    async def nyt_state(self, state) -> List[NewYorkTimesState]:
        """
        Get the data for a single state from New York Times
        """
        endpoint = NYT_SINGLE_STATE.format(self.api_url, state)
        data = await self.request_client.make_request(endpoint)

        return [self._compile_nyt_state(d) for d in data]


    async def nyt_counties(self) -> List[NewYorkTimesCounty]:
        """
        Get the data for all counties within all US states from NYT
        """
        endpoint = NYT_ALL_COUNTIES.format(self.api_url)
        data = await self.request_client.make_request(endpoint)

        county_list = self._compile_county_list(data)

        return county_list


    async def nyt_county(self, county) -> NewYorkTimesCounty:
        """
        Get the data for all counties within all US states from NYT
        """
        endpoint = NYT_SINGLE_COUNTY.format(self.api_url, county)
        data = await self.request_client.make_request(endpoint)

        county_data = self._compile_nyt_county(data)

        return county_data


    async def apple_countries(self) -> List[str]:
        """
        Get the list of countries supported by Apple's mobility data set
        """
        endpoint = APPLE_COUNTRIES.format(self.api_url)
        data = await self.request_client.make_request(endpoint)

        return data


    async def apple_subregions(self, country) -> AppleSubregions:
        """
        Get the list of supported subregions for a country within Apple's mobility data set
        """
        endpoint = APPLE_SUBREGIONS.format(self.api_url, country)
        data = await self.request_client.make_request(endpoint)

        return AppleSubregions(
            data.get("country"),
            data.get("subregions")
        )


    async def apple_mobility_data(self, country, subregion) -> AppleSubregion:
        """
        Get the statistics for the specified subregion
        """
        endpoint = APPLE_SINGLE_SUBREGION.format(self.api_url, country, subregion)
        data = await self.request_client.make_request(endpoint)

        subregion_string = data.get("subregion")

        statistics = [self._compile_apple_stats(stats) for stats in data["data"]]

        return AppleSubregion(
            subregion_string,
            statistics
        )


    async def gov_countries(self) -> List[str]:
        """
        Get a list of countries supported by Governmental data
        """
        endpoint = GOV_ALL.format(self.api_url)
        data = await self.request_client.make_request(endpoint)

        return data


    async def gov(self, country, **kwargs) -> Dict:
        """
        Get the data from the Government of a specified country.

        The data comes from the website of the government of each country so it is difficult to produce a standardised format.
        As a result, we cannot create a unified class for such data. Therefore, returned data will be a list of dicts.

        To get a list of attributes, you can use `list(data.keys())`
        """
        allow_none = kwargs.get('allow_none', False)

        if allow_none:
            self._check_allow_none(allow_none)

        allow_none = str(allow_none).lower()
        params = {"allowNull": allow_none}

        endpoint = GOV_COUNTRY.format(self.api_url, country)
        data = await self.request_client.make_request(endpoint, params)

        return data


    async def vaccine(self) -> Vaccines:
        """
        Get the data about vaccine trials for Covid.
        Data sourced from https://www.raps.org/news-and-articles/news-articles/2020/3/covid-19-vaccine-tracker
        """
        endpoint = VACCINE.format(self.api_url)
        data = await self.request_client.make_request(endpoint)

        return self._compile_vaccines(data)


    async def vaccine_coverage(self, last_days='all') -> List[VaccineTimeline]:
        """
        Get global vaccine coverage data.
        """
        endpoint = COVERAGE_ALL.format(self.api_url)
        params = {'lastdays': last_days}
        data = await self.request_client.make_request(endpoint, params=params)

        return self._compile_vax_tl(data)


    async def vaccine_countries(self, last_days='all') -> List[VaccineCountry]:
        """
        Get vaccination data for all countries.
        """
        endpoint = COVERAGE_COUNTRIES.format(self.api_url)
        params = {'lastdays': last_days}
        data = await self.request_client.client.make_request(endpoint, params=params)

        return [self._compile_vax_country(country) for country in data]


    async def vaccine_country(self, country, last_days='all') -> VaccineCountry:
        """
        Get vaccination data for a specific country.
        """
        endpoint = COVERAGE_COUNTRY.format(self.api_url, country)
        params = {'lastdays': last_days}
        data = self.request_client.make_request(endpoint, params=params)

        return self._compile_vax_country(data)


    async def therapeutics(self):
        raise NotImplementedError