from datetime import datetime, timezone
from .request import RequestClient
from .statistics import *
from .exceptions import NotFound, BadSortParameter, BadYesterdayParameter, BadAllowNoneParameter
from .endpoints import *


class Client:
    """
    Handles interactions with the NovelCOVID API
    """
    def __init__(self, api_url='https://disease.sh/v2'):
        self.api_url = api_url
        self.request_client = RequestClient()

    
    def _check_sort(self, sort):
        if sort not in ["cases", "deaths", "recovered", "active", "tests",
                        "critical", "deathsPerOneMillion", "testsPerOneMillion",
                        "todayCases", "todayDeaths", "casesPerOneMillion", "active"]:
            raise BadSortParameter('Invalid sort parameter.')


    def _check_yesterday(self, value):
        if not isinstance(value, bool):
            raise BadYesterdayParameter('Value for yesterday should either be True or False')


    def _check_allow_none(self, value):
        if not isinstance(value, bool):
            raise BadAllowNoneParameter('Value for allow_none should either be True or False')


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
        today_cases = country_stats.get("todayCases", 0)
        today_deaths = country_stats.get("todayDeaths", 0)
        total_critical = country_stats.get("critical", 0)
        active = country_stats.get("active", 0)
        tests = country_stats.get("tests", 0)
        cases_per_million = country_stats.get("casesPerOneMillion", 0)
        deaths_per_million = country_stats.get("deathsPerOneMillion", 0)
        tests_per_million = country_stats.get("testsPerOneMillion", 0)
        recoveries_per_million = country_stats.get("recoveredPerOneMillion", 0)
        critical_per_million = country_stats.get("criticalPerOneMillion", 0)
        active_per_million = country_stats.get("activePerOneMillion", 0)
        continent = country_stats.get("continent")
        population = country_stats.get("population", 0)
        updated_epoch = country_stats.get("updated", 0)
        updated = datetime.utcfromtimestamp(updated_epoch/1000.0)

        countryInfo = country_stats["countryInfo"]

        info = self._compile_countryInfo(countryInfo)
        
        return CountryStatistics(
            info,
            country_name,
            total_country_cases,
            total_country_deaths,
            total_country_recoveries,
            today_cases,
            today_deaths,
            total_critical,
            active,
            tests,
            cases_per_million,
            deaths_per_million,
            tests_per_million,
            recoveries_per_million,
            critical_per_million,
            active_per_million,
            continent,
            population,
            updated
        )


    def _compile_state(self, state_dict):
        state_name = state_dict.get("state")
        total_state_cases = state_dict.get("cases", 0)
        total_state_deaths = state_dict.get("deaths", 0)
        today_cases = state_dict.get("todayCases", 0)
        today_deaths = state_dict.get("todayDeaths", 0)
        active = state_dict.get("active", 0)
        tests = state_dict.get("tests", 0)
        cases_per_million = state_dict.get("casesPerOneMillion", 0)
        deaths_per_million = state_dict.get("deathsPerOneMillion", 0)
        tests_per_million = state_dict.get("testsPerOneMillion", 0)

        state_stats = StateStatistics(
        state_name,
        total_state_cases,
        total_state_deaths,
        today_cases,
        today_deaths,
        active,
        tests,
        cases_per_million,
        deaths_per_million,
        tests_per_million
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

        return HistoricalStatistics(
            country_name,
            case_history,
            death_history,
            recovery_history,
            province_name
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

        stat = JhuCsseStatistics(
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
        today_cases = data.get("todayCases", 0)
        today_deaths = data.get("todayDeaths", 0)
        critical = data.get("critical", 0)
        updated_epoch = data.get("updated", 0)
        active = data.get("active", cases-deaths-recoveries)
        tests = data.get("tests", 0)
        cases_per_million = data.get("casesPerOneMillion", 0)
        deaths_per_million = data.get("deathsPerOneMillion", 0)
        tests_per_million = data.get("testsPerOneMillion", 0)
        active_per_million = data.get("activePerOneMillion", 0)
        recoveries_per_million = data.get("recoveredPerOneMillion", 0)
        critical_per_million = data.get("criticalPerOneMillion", 0)
        population = data.get("population", 0)
        updated = datetime.utcfromtimestamp(updated_epoch/1000.0)

        return ContinentStatistics(
            name,
            countries,
            cases,
            deaths,
            recoveries,
            critical,
            active,
            tests,
            today_cases,
            today_deaths,
            cases_per_million,
            deaths_per_million,
            tests_per_million,
            active_per_million,
            recoveries_per_million,
            critical_per_million,
            population,
            updated
        )    


    def _compile_state_list(self, data):
        dates = []

        for d in data:
            state = self._compile_nyt_state(d)
            dates.append(state)
        
        return dates


    def _compile_county_list(self, data):
        dates = []

        for d in data:
            county = self._compile_nyt_county(d)
            dates.append(county)
        
        return dates
    
    
    def _compile_nyt_state(self, data):
        date = data.get('date')
        state = data.get('state')
        fips = data.get('fips')
        cases = data.get('cases')
        deaths = data.get('deaths')

        if date:
            date = datetime.strptime(date, "%Y-%m-%d")

        return NewYorkTimesStateStatistics(
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

        return NewYorkTimesCountyStatistics(
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

        return AppleMobilityData(
            name,
            _type,
            date,
            driving,
            transit,
            walking
        )
    
    
    async def all(self, **kwargs):
        """
        Get the global stats for Coronavirus COVID-19
        """
        yesterday = kwargs.get('yesterday', False)
        allow_none = kwargs.get('allow_none', False)

        endpoint = GLOBAL_DATA.format(self.api_url)

        if yesterday:
            self._check_yesterday(yesterday)
        
        if allow_none:
            self._check_allow_none(allow_none)
        
        yesterday = str(yesterday).lower()
        allow_none = str(allow_none).lower()
        params = {"yesterday": yesterday, "allowNull": allow_none}

        global_data = await self.request_client.make_request(endpoint, params)

        cases = global_data.get("cases", 0)
        deaths = global_data.get("deaths", 0)
        recoveries = global_data.get("recovered", 0)
        today_cases = global_data.get("todayCases", 0)
        today_deaths = global_data.get("todayDeaths", 0)
        total_critical = global_data.get("critical", 0)
        updated_epoch = global_data.get("updated", 0)
        active = global_data.get("active", 0)
        tests = global_data.get("tests", 0)
        cases_per_million = global_data.get("casesPerOneMillion", 0)
        deaths_per_million = global_data.get("deathsPerOneMillion", 0)
        tests_per_million = global_data.get("testsPerOneMillion", 0)
        active_per_million = global_data.get("activePerOneMillion", 0)
        recoveries_per_million = global_data.get("recoveredPerOneMillion", 0)
        critical_per_million = global_data.get("criticalPerOneMillion", 0)
        population = global_data.get("population", 0)
        infected_countries = global_data.get("affectedCountries")
        updated = datetime.utcfromtimestamp(updated_epoch/1000.0)

        return GlobalStatistics(
            cases,
            deaths,
            recoveries,
            today_cases,
            today_deaths,
            total_critical,
            active,
            tests,
            cases_per_million,
            deaths_per_million,
            tests_per_million,
            active_per_million,
            recoveries_per_million,
            critical_per_million,
            population,
            infected_countries,
            updated,
            )

    
    async def get_country_data(self, country, **kwargs):
        """
        Get the data for a specific country.
        """
        yesterday = kwargs.get('yesterday', False)
        allow_none = kwargs.get('allow_none', False)

        endpoint = COUNTRY_DATA.format(self.api_url, country)

        if yesterday:
            self._check_yesterday(yesterday)
        
        if allow_none:
            self._check_allow_none(allow_none)
        
        yesterday = str(yesterday).lower()
        allow_none = str(allow_none).lower()
        params = {"yesterday": yesterday, "allowNull": allow_none}

        country_stats = await self.request_client.make_request(endpoint, params)

        return self._compile_country_data(country_stats)


    async def get_country_list(self, *countries, **kwargs):
        """
        Get the data for more than one country, but not necessarily all of them.
        """
        yesterday = kwargs.get('yesterday', False)
        allow_none = kwargs.get('allow_none', False)
        country_list = ','.join(map(str, countries))

        endpoint = COUNTRY_DATA.format(self.api_url, country_list)

        if yesterday:
            self._check_yesterday(yesterday)

        if allow_none:
            self._check_allow_none(allow_none)
        
        yesterday = str(yesterday).lower()
        allow_none = str(allow_none).lower()
        params = {"yesterday": yesterday, "allowNull": allow_none}
            
        data = await self.request_client.make_request(endpoint, params)

        if isinstance(data, dict):
            return self._compile_country_data(data)
        
        returned_countries = []

        for country in data:
            returned_countries.append(
                self._compile_country_data(country)
            )
        return returned_countries

    
    async def get_all_countries(self, **kwargs):
        """
        Get the data for every infected country.
        """
        yesterday = kwargs.get('yesterday', False)
        allow_none = kwargs.get('allow_none', False)
        sort = kwargs.get('sort', None)

        endpoint = ALL_COUNTRIES.format(self.api_url)
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
            
        all_countries = await self.request_client.make_request(endpoint, params)

        list_of_countries = []

        for c in all_countries:
            list_of_countries.append(self._compile_country_data(c))

        return list_of_countries
    
    
    async def get_all_states(self, **kwargs):
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

        state_data = []

        for state in state_info:
            state_stats = self._compile_state(state)
            state_data.append(state_stats)

        return state_data

    
    async def get_single_state(self, state, **kwargs):
        """
        Get the stats for a specific province of a country
        """
        yesterday = kwargs.get('yesterday', False)
        allow_none = kwargs.get('allow_none', False)

        endpoint = SINGLE_STATE.format(self.api_url, state)

        if yesterday:
            self._check_yesterday(yesterday)
        
        if allow_none:
            self._check_allow_none(allow_none)
        
        yesterday = str(yesterday).lower()
        allow_none = str(allow_none).lower()
        params = {"yesterday": yesterday, "allowNull": allow_none}

        state_info = await self.request_client.make_request(endpoint, params)

        compiled_state = self._compile_state(state_info)

        return compiled_state


    async def get_state_list(self, *states, **kwargs):
        """
        Get the stats for more than one state
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
        
        returned_states = []

        for state in data:
            returned_states.append(
                self._compile_state(state)
            )
        return returned_states


    async def get_country_history(self, country='all', last_days='all'):
        """
        Get historical data for a specific country or globally.
        Defaults to 'all' in order to get global data. This can be overridden by the client.
        """
        endpoint = HISTORICAL_COUNTRY.format(self.api_url, country)
        params = {"lastdays": last_days}

        historical_stats = await self.request_client.make_request(endpoint, params)

        return self._generate_history(historical_stats)


    async def get_province_history(self, country, province, last_days='all'):
        """
        Get the historical data for a province within a country.
        """
        endpoint = HISTORICAL_PROVINCE.format(self.api_url, country, province)
        params = {"lastdays": last_days}

        data = await self.request_client.make_request(endpoint, params)

        return self._generate_history(data)


    async def get_state_county_history(self, state, county, last_days='all'):
        """
        Get the historical data for a county within a US state.
        """
        endpoint = STATE_COUNTY.format(self.api_url, state)
        params = {"lastdays": last_days}

        data = await self.request_client.make_request(endpoint, params)
        
        try:
            matching_county = next(place for place in data if place["province"].lower() == state.lower() \
            and place["county"].lower() == county.lower())
        except StopIteration:
            raise NotFound('Nothing found for specified county.')

        return self._generate_history(matching_county, True)

    
    async def get_jhu_csse_data(self):
        """
        Get data from the JHU CSSE.
        This includes province data for several countries
        """
        endpoint = JHU_CSSE.format(self.api_url)
        data = await self.request_client.make_request(endpoint)

        statistics = []

        for cp in data:
            statistics.append(self._compile_jhu_data(cp))

        return statistics


    async def get_jhu_county_data(self, state, county):
        """
        Get the data for a specific county within a US state.
        """
        endpoint = JHU_SINGLE_COUNTY.format(self.api_url, county)

        all_matching_counties = await self.request_client.make_request(endpoint)

        try:
            matching_county = next(place for place in all_matching_counties if place["province"].lower() == state.lower() \
            and place["county"].lower() == county.lower())
        except StopIteration:
            raise NotFound('Nothing found for specified county.')

        return self._compile_jhu_data(matching_county)

    
    async def get_jhu_all_counties(self):
        """
        Get the data for every single county in the US provided by JHU.
        """
        endpoint = JHU_ALL_COUNTIES.format(self.api_url)

        data = await self.request_client.make_request(endpoint)

        places = []

        for place in data:
            places.append(self._compile_jhu_data(place))

        return places

    
    async def get_all_continents(self, **kwargs):
        """
        Get the statistics for world continents.
        """
        yesterday = kwargs.get('yesterday', False)
        sort = kwargs.get('sort', None)
        allow_none = kwargs.get('allow_none', False)

        endpoint = ALL_CONTINENTS.format(self.api_url)
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

        data = await self.request_client.make_request(endpoint, params)

        continents = []

        for c in data:
            continents.append(self._compile_continent(c))

        return continents


    async def get_single_continent(self, continent, **kwargs):
        """
        Get the statistics for a single continent.
        """
        yesterday = kwargs.get('yesterday', False)
        allow_none = kwargs.get('allow_none', False)

        endpoint = CONTINENT_DATA.format(self.api_url)
        params = None

        if yesterday:
            self._check_yesterday(yesterday)

        yesterday = str(yesterday).lower()
        allow_none = str(allow_none).lower()
        params = {"yesterday": yesterday, "allowNull": allow_none}

        data = await self.request_client.make_request(endpoint, params)

        return self._compile_continent(data)


    async def get_nyt_usa_data(self):
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
                NewYorkTimesUsaStatistics(
                    date,
                    cases,
                    deaths
                )
            )

        return dates


    async def get_nyt_all_states(self):
        """
        Get the data for all states from New York Times
        """
        endpoint = NYT_ALL_STATES.format(self.api_url)
        data = await self.request_client.make_request(endpoint)

        states_list = self._compile_state_list(data)

        return states_list


    async def get_nyt_single_state(self, state):
        """
        Get the data for a single state from New York Times
        """
        endpoint = NYT_SINGLE_STATE.format(self.api_url, state)
        data = await self.request_client.make_request(endpoint)

        state_data = self._compile_state_list(data)

        return state_data

    
    async def get_nyt_all_counties(self):
        """
        Get the data for all counties within all US states from NYT
        """
        endpoint = NYT_ALL_COUNTIES.format(self.api_url)
        data = await self.request_client.make_request(endpoint)

        county_list = self._compile_county_list(data)

        return county_list


    async def get_nyt_single_county(self, county):
        """
        Get the data for all counties within all US states from NYT
        """
        endpoint = NYT_SINGLE_COUNTY.format(self.api_url, county)
        data = await self.request_client.make_request(endpoint)

        county_data = self._compile_county_list(data)

        return county_data


    async def apple_all_countries(self):
        """
        Get the list of countries supported by Apple's mobility data set
        """
        endpoint = APPLE_COUNTRIES.format(self.api_url)
        data = await self.request_client.make_request(endpoint)

        return data


    async def apple_subregions(self, country):
        """
        Get the list of supported subregions for a country within Apple's mobility data set
        """
        endpoint = APPLE_SUBREGIONS.format(self.api_url, country)
        data = await self.request_client.make_request(endpoint)

        return AppleSubregions(
            data.get("country"),
            data.get("subregions")
        )

    
    async def apple_mobility_data(self, country, subregion):
        """
        Get the statistics for the specified subregion
        """
        endpoint = APPLE_SINGLE_SUBREGION.format(self.api_url, country, subregion)
        data = await self.request_client.make_request(endpoint)

        subregion_string = data.get("subregion")

        statistics = []

        for stats in data["data"]:
            statistics.append(self._compile_apple_stats(stats))

        return AppleSubregionStatistics(
            subregion_string,
            statistics
        )


    async def gov_supported_countries(self):
        """
        Get a list of countries supported by Governmental data
        """
        endpoint = GOV_ALL.format(self.api_url)
        data = await self.request_client.make_request(endpoint)

        return data


    async def gov_country(self, country, **kwargs):
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