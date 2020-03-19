from datetime import datetime
import aiohttp
from .utils import format_number
from .statistics import GlobalStatistics, CountryStatistics

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

        return GlobalStatistics(cases,
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
                raise APIerror('Failed to get country data data.')

            country_stats = await resp.json()

        country_name = country_stats.get("country", "Null")
        total_country_cases = country_stats.get("cases", 0)
        total_country_deaths = country_stats.get("deaths", 0)
        total_country_recoveries = country_stats.get("recovered", 0)
        today_cases = country_stats.get("todayCases", 0)
        today_deaths = country_stats.get("todayDeaths", 0)
        total_critical = country_stats.get("critical", 0)
        cases_per_million = country_stats.get("casesPerOneMillion", 0)
        
        return CountryStatistics(country_name,
            total_country_cases,
            total_country_deaths,
            total_country_recoveries,
            today_cases, today_deaths,
            total_critical,
            cases_per_million
            )
        