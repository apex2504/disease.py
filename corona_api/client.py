from datetime import datetime
import aiohttp
from .statistics import GlobalStatistics, CountryStatistics, StateStatistics, CountryHistory, HistoryEntry

class APIerror(Exception):
    pass


class Client:
    """
    Handles interactions with the corona.lmao.ninja API
    """
    def __init__(self):
        self.session = aiohttp.ClientSession()

        self.global_data = 'https://corona.lmao.ninja/all'
        self.all_countries = 'https://corona.lmao.ninja/countries'
        self.country_data = 'https://corona.lmao.ninja/countries/{}'
        self.states = 'https://corona.lmao.ninja/states'
        self.historical = 'https://corona.lmao.ninja/v2/historical/{}'


    async def all(self):
        """
        Get the global stats for Coronavirus COVID-19
        """
        async with self.session.get(self.global_data) as resp:
            if not resp.status == 200:
                raise APIerror('Failed to get global data.')

            global_data = await resp.json()

        async with self.session.get(self.all_countries) as resp:
            if not resp.status == 200:
                raise APIerror('Failed to get global data.')

            country_data = await resp.json()

        cases = global_data.get("cases", 0)
        deaths = global_data.get("deaths", 0)
        recoveries = global_data.get("recovered", 0)
        updated_epoch = global_data.get("updated", None)
        updated = datetime.fromtimestamp(updated_epoch/1000.0)

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
            updated
            )

    
    async def get_country_data(self, country):
        """
        Get the data for a specific country.
        """
        async with self.session.get(self.country_data.format(country)) as resp:
            if not resp.status == 200:
                raise APIerror('Failed to get country data.')

            country_stats = await resp.json()

        country_name = country_stats.get("country", "Null")
        total_country_cases = country_stats.get("cases", 0)
        total_country_deaths = country_stats.get("deaths", 0)
        total_country_recoveries = country_stats.get("recovered", 0)
        today_cases = country_stats.get("todayCases", 0)
        today_deaths = country_stats.get("todayDeaths", 0)
        total_critical = country_stats.get("critical", 0)
        cases_per_million = country_stats.get("casesPerOneMillion", 0)
        flag = country_stats["countryInfo"].get("flag", None)
        
        return CountryStatistics(
            country_name,
            total_country_cases,
            total_country_deaths,
            total_country_recoveries,
            today_cases,
            today_deaths,
            total_critical,
            cases_per_million,
            flag
            )
        
    
    async def get_state_info(self, state):
        """
        Get the stats for a specific province of a country
        """
        async with self.session.get(self.states) as resp:
            if not resp.status == 200:
                raise APIerror('Failed to get country data.')

            all_states = await resp.json()
        
        state = state.title()

        state_info = next(s for s in all_states if s["state"] == state)

        state_name = state_info.get("state", "Null")
        total_state_cases = state_info.get("cases", 0)
        total_state_deaths = state_info.get("deaths", 0)
        total_state_recoveries = state_info.get("recovered", 0)
        today_cases = state_info.get("todayCases", 0)
        today_deaths = state_info.get("todayDeaths", 0)
        active = state_info.get("active", 0)

        return StateStatistics(
            state_name,
            total_state_cases,
            total_state_deaths,
            total_state_recoveries,
            today_cases,
            today_deaths,
            active
            )
        

    async def get_history(self, country):
        """
        Get historical data for a specific country.
        """
        async with self.session.get(self.historical.format(country)) as resp:
            if not resp.status == 200:
                raise APIerror('Failed to get historical data.')

            historical_stats = await resp.json()

        case_history = []
        death_history = []
        #recovery_history = []
                
        name = historical_stats["country"]

        if not historical_stats["timeline"]["cases"]:
            raise APIerror('Couldn\'t get stats for given country')

        for date in list(historical_stats["timeline"]["cases"].keys()): #pass on all historical data. let the client decide how much of it they want
            case_history.append(HistoryEntry(date, historical_stats["timeline"]["cases"][date]))
            death_history.append(HistoryEntry(date, historical_stats["timeline"]["deaths"][date]))
            #recovery_history.append(HistoryEntry(date, historical_stats["timeline"]["recovered"][date])) #history v2 no longer includes recovery data

        return CountryHistory(name, case_history, death_history) #, recovery_history)


    async def get_sorted_data(self, sort):
        """
        Get the data for all countries sorted by the parameter given.
        When sorted alphabetically, data is returned Z-A rather than A-Z.
        If the user wishes to reverse it, they are able to use list.reverse()
        """
        if sort != "cases" and sort != "deaths" and sort != "recovered" and sort != "alphabetical" and sort != "country"\
        and sort != "todayCases" and sort != "todayDeaths" and sort != "casesPerOneMillion":
            raise APIerror('Invalid sort parameter')
        
        if sort == "alphabetical":
            sort = "country"

        async with self.session.get('{}?sort={}'.format(self.all_countries, sort)) as resp:
            if not resp.status == 200:
                raise APIerror('Unexpected error, code {}'.format(resp.status))

            data = await resp.json()

        sorted_data = []

        for country in data:
            c = CountryStatistics(
                country["country"],
                country["cases"],
                country["deaths"],
                country["recovered"],
                country["todayCases"],
                country["todayDeaths"],
                country["critical"],
                country["casesPerOneMillion"],
                country["countryInfo"]["flag"]
            )
            sorted_data.append(c)
        
        return sorted_data
