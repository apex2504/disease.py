import discord
from discord.ext import commands
import corona_api
import asyncio


#the following code sucks
def generate_base_embed(embed, data):

    """
    Generate a basic embed with generic data.

    Params:
        embed:
            The discord.Embed we will be editing
        data:
            The data containing the figures and stats.
    """

    embed.add_field(name="Total cases", value = corona_api.format_number(data.cases))
    embed.add_field(name="New cases today", value = corona_api.format_number(data.today_cases))
    embed.add_field(name="Total deaths", value = corona_api.format_number(data.deaths))
    embed.add_field(name="New deaths today", value = corona_api.format_number(data.today_deaths))
    embed.add_field(name="Number of tests", value = corona_api.format_number(data.tests))

def generate_all_embed(embed, data):
    
    """
    Generate the embed which is used when getting global data.

    Params:
        embed:
            The discord.Embed we will be editing
        data:
            The data containing the figures and stats.
    """
    
    embed.add_field(name="Total recoveries", value = corona_api.format_number(data.recoveries))
    embed.add_field(name="Total critical cases", value = corona_api.format_number(data.critical))
    embed.add_field(name="Active cases", value = corona_api.format_number(data.active))
    embed.add_field(name="Last updated", value = corona_api.format_date(data.updated))

def generate_country_embed(embed, data, yesterdays_data):
    
    """
    Generate the embed which is sent when getting data for a specific country.

    Params:
        embed:
            The discord.Embed we will be editing.
        data:
            The data containing the figures and stats.
        yesterdays_data:
            The data containing yesterday's figures and stats.
    """
    
    embed.add_field(name="New cases yesterday", value = corona_api.format_number(yesterdays_data.today_cases))
    embed.add_field(name="New deaths yesterday", value = corona_api.format_number(yesterdays_data.today_deaths))
    embed.add_field(name="Total recoveries", value = corona_api.format_number(data.recoveries))
    embed.add_field(name="Total critical cases", value = corona_api.format_number(data.critical))
    embed.add_field(name="Active cases", value = corona_api.format_number(data.active))
    embed.add_field(name="Cases per million people", value = corona_api.format_number(data.cases_per_million))
    embed.add_field(name="Deaths per million people", value = corona_api.format_number(data.deaths_per_million))
    embed.add_field(name="Last updated", value = corona_api.format_date(data.updated))
    embed.description = "**Country: {}**".format(data.name)
    embed.set_thumbnail(url=data.info.flag)

def generate_state_embed(embed, data, yesterday):
    
    """
    Generate the embed which is used when getting data about US states.

    Params:
        embed:
            The discord.Embed we will be editing.
        data:
            The data containing the figures and stats.
        yesterday:
            The data containing yesterday's figures and stats.
    """
    
    embed.add_field(name="New cases yesterday", value = corona_api.format_number(yesterday.today_cases))
    embed.add_field(name="New deaths yesterday", value = corona_api.format_number(yesterday.today_deaths))
    embed.add_field(name="Active cases", value = corona_api.format_number(data.active))
    embed.description = "**State: {}**".format(data.name)


class Coronavirus(commands.Cog):

    """
    Cog for Coronavirus data.
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.corona = corona_api.Client()

    async def _jhucsse(self, country, province):
            
        """
        This is not a command but is used to get data from the JHU CSSE. 
        Used when we want data for specific provinces.

        Params:
            country:
                The name of the country
            province:
                The name of the province we want data for.
        """
    
        data = await self.corona.get_jhu_csse_data() #get all data from the JHU CSSE

        if country.lower() == 'uk':
            country = 'united kingdom' #corrections

        relevant = next(cp for cp in data if cp.country_name.lower() == country.lower()\
            and str(cp.province_name).lower() == province.lower()) #filter data for the relevant province
        
        embed = discord.Embed(title="Coronavirus (COVID-19) stats", color=65280)
        embed.set_footer(text="These stats are what has been officially confirmed. It is possible that real figures are different.")
        embed.description = "**Country: {}**\n**Province: {}**".format(relevant.country_name, relevant.province_name)

        embed.add_field(name="Total cases", value = corona_api.format_number(relevant.confirmed_cases))
        embed.add_field(name="Total deaths", value = corona_api.format_number(relevant.deaths))
        embed.add_field(name="Total recoveries", value = corona_api.format_number(relevant.recoveries))
        embed.add_field(name="Active cases", value = corona_api.format_number(relevant.confirmed_cases-relevant.deaths-relevant.recoveries))
        embed.add_field(name="Last updated", value = corona_api.format_date(relevant.updated))
        #this is different from everything else due to the data the API reports, so we cant use a generic embed builder.
        return embed


    @commands.command(name="coronavirus", aliases=["cv", "corona"])
    async def coronavirus(self, ctx, country=None, *, province=None):

        """
        Get the statistics for Coronavirus (COVID-19) for a specified country.

        Params:
            ctx:
                The context for the command.
            country:
                The country to get the stats for. If None, get global stats.
            province:
                The province to get stats for. Can also be a US state.
        """
    
        if not country:
            data = await self.corona.all(allow_none=True)

        elif province:
            if (country.lower() == "us" or country.lower() == "usa"):
                data = await self.corona.get_single_state(province)
                
            else:
                embed = await self._jhucsse(country, province)
                return await ctx.send(embed=embed)

        else:
            data = await self.corona.get_country_data(country, allow_none=True)

        embed = discord.Embed(title="Coronavirus (COVID-19) stats", color=65280)
        embed.set_footer(text="These stats are what has been officially confirmed. It is possible that real figures are different.")

        generate_base_embed(embed, data)

        if isinstance(data, corona_api.GlobalStatistics):
            generate_all_embed(embed, data)

        elif isinstance(data, corona_api.CountryStatistics):
            yesterdays_data = await self.corona.get_country_data(country, yesterday=True, allow_none=True)
            generate_country_embed(embed, data, yesterdays_data)

        elif isinstance(data, corona_api.StateStatistics):
            yesterdays_data = await self.corona.get_single_state(province, yesterday=True, allow_none=True)
            generate_state_embed(embed, data, yesterdays_data)

        await ctx.send(embed=embed)


    @commands.command(name="coronavirushistory", aliases=["cvhistory", "cvh", "coronahistory"])
    async def coronavirushistory(self, ctx, country="all", *, province=None):
        
        """
        Get the history for Coronavirus (COVID-19) for a specified country.
        This will display the past 14 days of data for cases, deaths and recoveries.

        Params:
            ctx:
                The context for the command.
            country:
                The country to get the history for. Defaults to all to get global history.
            province:
                The province to get history for.
        """

        if 'korea' in country.lower():
            country = 'korea, south' #no stats for north korea

        if province:
            data = await self.corona.get_province_history(country, province, 14) #get the history for the given country with province
        else:
            data = await self.corona.get_country_history(country, 14) #if no province given, get the data for whole country

        name = data.name
        prov = str(data.province).title()
        embed = discord.Embed(title="Coronavirus history", description="**Country: {}**\n**Province: {}**".format(name, prov), color=65280)
        embed.set_footer(text='These stats are what has been officially confirmed. It is possible that real figures are different.')

        case_history_value = ''
        death_history_value = ''
        recovery_history_value = ''

        for i in range(14): #get the previous 2 weeks
            case_history_value = "{}\n**{}:** \
                {}".format(case_history_value, data.case_history[i].date,
                corona_api.format_number(data.case_history[i].value) if data.case_history[i].value is not None else 'Unknown')
            death_history_value = "{}\n**{}:** \
                {}".format(death_history_value, data.death_history[i].date,
                corona_api.format_number(data.death_history[i].value) if data.death_history[i].value is not None else 'Unknown')
            recovery_history_value = "{}\n**{}:** \
                {}".format(recovery_history_value, data.recovery_history[i].date,
                corona_api.format_number(data.recovery_history[i].value) if data.recovery_history[i].value is not None else 'Unknown')

        embed.add_field(name="Number of cases", value=case_history_value)
        embed.add_field(name="Number of deaths", value=death_history_value)
        embed.add_field(name="Number of recoveries",value=recovery_history_value)

        await ctx.send(embed=embed)


    @commands.command(name="coronavirusleaderboard", aliases=["cvlb", "coronaleaderboard", "coronatop", "cvtop"])
    async def coronavirusleaderboard(self, ctx, sort="cases"):

        """
        Get the top 15 countries sorted by a certain parameter.

        Params:
            ctx:
                The context for the command.
            sort:
                The parameter by which to sort the data.
                corona_api.exceptions.BadSortParameter will be raised if an invalid one is used.
                Defaults to sort by the number of cases.
        """

        data = await self.corona.get_all_countries(sort=sort)

        embed = discord.Embed(title="Top 15 cases", description="", color=65280)
        embed.set_footer(text='These stats are what has been officially confirmed. It is possible that real figures are different.')

        for i in range(1,16): #top 15
            country = data[i-1]
            name = country.name
            #sometimes the stats are null/None.
            if country.cases is None:
                cases = 'Unknown'
            else:
                cases = corona_api.format_number(country.cases)
            if country.deaths is None:
                deaths = 'Unknown'
            else:
                deaths = corona_api.format_number(country.deaths)

            embed.description = '{}**{}. {}:** {} cases, {} deaths.\n'.format(
                embed.description, i, name, cases, deaths
            )
        
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Coronavirus(bot))