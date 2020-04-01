from datetime import datetime, timezone
from .request import RequestClient
from .statistics import GlobalStatistics, CountryStatistics, CountryInfo, StateStatistics, HistoricalStatistics, HistoryEntry, JhuCsseStatistics
from .exceptions import BadSortParameter
from .endpoints import *


class Client:
    """
    Handles interactions with the corona.lmao.ninja API
    """
    def __init__(self, api_url='https://corona.lmao.ninja'):
        self.api_url = api_url
        self.request_client = RequestClient()


    async def all(self):
        """
        Get the global stats for Coronavirus COVID-19
        """
        global_endpoint = GLOBAL_DATA.format(self.api_url)
        country_endpoint = ALL_COUNTRIES.format(self.api_url)

        global_data = await self.request_client.make_request(global_endpoint)
        country_data = await self.request_client.make_request(country_endpoint)

        cases = global_data.get("cases", 0)
        deaths = global_data.get("deaths", 0)
        recoveries = global_data.get("recovered", 0)
        updated_epoch = global_data.get("updated", 0)
        active = global_data.get("active", cases-deaths-recoveries)
        infected_countries = global_data.get("affectedCountries")
        updated = datetime.utcfromtimestamp(updated_epoch/1000.0)

        today_cases = 0
        today_deaths = 0
        total_critical = 0

        for c in country_data:
            today_cases += c["todayCases"] if c["todayCases"] else 0
            today_deaths += c["todayDeaths"] if c["todayDeaths"] else 0
            total_critical += c["critical"] if c["critical"] else 0

        return GlobalStatistics(
            cases,
            deaths,
            recoveries,
            today_cases,
            today_deaths,
            total_critical,
            active,
            infected_countries,
            updated
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
        country_name = country_stats.get("country", "Null")
        total_country_cases = country_stats.get("cases", 0)
        total_country_deaths = country_stats.get("deaths", 0)
        total_country_recoveries = country_stats.get("recovered", 0)
        today_cases = country_stats.get("todayCases", 0)
        today_deaths = country_stats.get("todayDeaths", 0)
        total_critical = country_stats.get("critical", 0)
        active = country_stats.get("active", 0)
        cases_per_million = country_stats.get("casesPerOneMillion", 0)
        deaths_per_million = country_stats.get("deathsPerOneMillion", 0)
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
            cases_per_million,
            deaths_per_million,
            updated,
        )

    
    async def get_country_data(self, country):
        """
        Get the data for a specific country.
        """
        endpoint = COUNTRY_DATA.format(self.api_url, country)
        country_stats = await self.request_client.make_request(endpoint)

        return self._compile_country_data(country_stats)

    
    async def get_all_countries(self):
        """
        Get the data for every infected country.
        """
        endpoint = ALL_COUNTRIES.format(self.api_url)
        all_countries = await self.request_client.make_request(endpoint)

        list_of_countries = []

        for c in all_countries:
            list_of_countries.append(self._compile_country_data(c))

        return list_of_countries
        
        
    async def _request_all_states(self):
        """
        Request the stats for all US states
        """
        endpoint = STATES.format(self.api_url)
        return await self.request_client.make_request(endpoint)


    def _compile_state(self, state_dict):
        state_name = state_dict.get("state")
        total_state_cases = state_dict.get("cases", 0)
        total_state_deaths = state_dict.get("deaths", 0)
        today_cases = state_dict.get("todayCases", 0)
        today_deaths = state_dict.get("todayDeaths", 0)
        active = state_dict.get("active", 0)

        state_stats = StateStatistics(
        state_name,
        total_state_cases,
        total_state_deaths,
        today_cases,
        today_deaths,
        active
        )

        return state_stats
    
    
    async def get_all_states(self):
        """
        Get the stats for all US states
        """
        state_info = await self._request_all_states()

        state_data = []

        for state in state_info:
            state_stats = self._compile_state(state)
            state_data.append(state_stats)

        return state_data

    
    async def get_single_state(self, state):
        """
        Get the stats for a specific province of a country
        """
        all_states = await self._request_all_states()

        state_info = next(s for s in all_states if s["state"].lower() == state.lower())

        compiled_state = self._compile_state(state_info)

        return compiled_state


    def _generate_history(self, historical_stats):
        case_history = []
        death_history = []
        recovery_history = []
                
        country_name = historical_stats.get("country", "Global")
        province_name = historical_stats.get("province")
        
        if "timeline" not in historical_stats: #if country was 'all'
            d = historical_stats
        
        else:
            d = historical_stats["timeline"]

        for date in list(d["cases"].keys()): #pass on all historical data. let the client decide how much of it they want
            case_history.append(HistoryEntry(date, d["cases"][date]))
            death_history.append(HistoryEntry(date, d["deaths"][date]))
            recovery_history.append(HistoryEntry(date, d["recovered"][date]))

        return HistoricalStatistics(
            country_name,
            case_history,
            death_history,
            recovery_history,
            province_name
            )


    async def get_country_history(self, country="all"):
        """
        Get historical data for a specific country or globally.
        Defaults to 'all' in order to get global data. This can be overridden by the client.
        """
        endpoint = HISTORICAL_COUNTRY.format(self.api_url, country)
        historical_stats = await self.request_client.make_request(endpoint)

        return self._generate_history(historical_stats)


    async def get_province_history(self, country, province):
        """
        Get the historical data for a province within a country.
        """
        endpoint = HISTORICAL_PROVINCE.format(self.api_url, country, province)
        data = await self.request_client.make_request(endpoint)

        return self._generate_history(data)


    async def get_sorted_data(self, sort='cases'):
        """
        Get the data for all countries sorted by the parameter given.
        When sorted alphabetically, data is returned Z-A rather than A-Z.
        If the user wishes to reverse it, they are able to use list.reverse()
        Defaults to sort by number of cases.
        """
        if sort not in ["cases", "deaths", "recovered", "alphabetical", "country",
                        "todayCases", "todayDeaths", "casesPerOneMillion", "active"]:
            raise BadSortParameter('Sort parameter must be one of: cases, deaths, recovered, alphabetical,\
country, todayCases, todayDeaths, casesPerOneMillion or active')
        
        endpoint = SORTED_COUNTRIES.format(self.api_url, sort)
        data = await self.request_client.make_request(endpoint)

        sorted_data = []

        for country in data:
            c = self._compile_country_data(country)
            sorted_data.append(c)
        
        return sorted_data

    
    async def get_jhu_csse_data(self):
        """
        Get data from the JHU CSSE.
        This includes province data for several countries
        """
        endpoint = JHU_CSSE.format(self.api_url)
        data = await self.request_client.make_request(endpoint)

        country = data.get("country")
        province = data.get("province")
        confirmed_cases = data["stats"].get("confirmed")
        deaths = data["stats"].get("deaths")
        recoveries = data["stats"].get("recovered")
        _lat = data["coordinates"].get("latitude")
        _long = data["coordinates"].get("longitude")

        updated = datetime.strptime(data.get('updatedAt'), '%Y-%m-%d %H:%M:%S')

        return JhuCsseStatistics(
            country,
            province,
            updated,
            confirmed_cases,
            deaths,
            recoveries,
            _lat,
            _long
            )