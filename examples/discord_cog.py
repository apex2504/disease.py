"""
This is an example cog for bots written in discord.py (pip install discord.py).
The cog only contains one command which gets the stats for the virus and outputs it in the channel.
"""

import discord
from discord.ext import commands
import corona_api

class Coronavirus(commands.Cog):

    """
    Cog for Coronavirus data.
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.corona = corona_api.Client()

    @commands.command(name="coronavirus", aliases=["cv", "corona"])
    async def coronavirus(self, ctx, country=None, *, state=None):

        """
        Get the statistics for Coronavirus (COVID-19) for a specified country.

        Params:
            ctx:
                The context for the command
            country:
                The country to get the stats for. If None, get global stats
            state:
                The US state to get the stats for.
        """
    
        if not country:
            data = await self.corona.all()

        elif (country.lower() == "us" or country.lower() == "usa"):
            if state:
                data = await self.corona.get_state_info(state)
                
            else:
                data = await self.corona.get_country_data(country)

        else:
            data = await self.corona.get_country_data(country)

        embed = discord.Embed(title="Coronavirus (COVID-19) stats", color=65280)
        embed.set_footer(text="These stats are what has been officially confirmed. It is possible that real figures are different.")

        embed.add_field(name="Total cases", value = corona_api.format_number(data.cases))
        embed.add_field(name="Cases today", value = corona_api.format_number(data.today_cases))
        embed.add_field(name="Total deaths", value = corona_api.format_number(data.deaths))
        embed.add_field(name="Deaths today", value = corona_api.format_number(data.today_deaths))
        embed.add_field(name="Total recoveries", value = corona_api.format_number(data.recoveries))

        if not isinstance(data, corona_api.StateStatistics):
            embed.add_field(name="Total critical cases", value = corona_api.format_number(data.critical))

        if isinstance(data, corona_api.GlobalStatistics):
            embed.add_field(name="Last updated", value = corona_api.format_date(data.updated))

        elif isinstance(data, corona_api.CountryStatistics):
            embed.add_field(name="Cases per million people", value = corona_api.format_number(data.cases_per_million))
            embed.description = "**Country: {}**".format(data.name)

        else:
            embed.add_field(name="Active cases", value=corona_api.format_number(data.active))
            embed.description = "**State: {}**".format(data.name)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Coronavirus(bot))