from datetime import datetime, timezone
from .influenzastatistics import *
from .influenzaendpoints import *


class Influenza:
    def __init__(self, api_url, request_client):
        self.api_url = api_url
        self.request_client = request_client


    async def ilinet(self) -> ILINet:
        """
        Get Influenza-like-illness data for the 2019 and 2020 outbreaks from the US Center for Disease Control
        """
        endpoint = FLU_ILINET.format(self.api_url)

        data = await self.request_client.make_request(endpoint)

        updated = datetime.utcfromtimestamp(data.get('updated')/1000)
        source = data.get('source')

        weeks = []
        for item in data["data"]:
            weeks.append(
                ILINetData(
                    item["week"],
                    {"0-4": item["age 0-4"],
                    "5-24": item["age 5-24"],
                    "25-49": item["age 25-49"],
                    "50-64": item["age 50-64"],
                    "64+": item["age 64+"]},
                    item["totalILI"],
                    item["totalPatients"],
                    ILIPercent(
                        item["percentWeightedILI"],
                        item["percentUnweightedILI"]
                    )
                )
            )

        return ILINet(
            updated,
            source,
            weeks
        )


    async def uscl(self) -> USCL:
        """
        Get Influenza report data for the 2019 and 2020 outbreaks from the US Center for Disease Control, reported by US clinical labs
        """
        endpoint = FLU_USCL.format(self.api_url)

        data = await self.request_client.make_request(endpoint)

        updated = datetime.utcfromtimestamp(data.get('updated')/1000)
        source = data.get('source')

        weeks = []
        for item in data["data"]:
            weeks.append(
                USCLData(
                    item["week"],
                    USCLTotal(
                        item["totalA"],
                        item["totalB"],
                        item["totalTests"]
                    ),
                    USCLPercent(
                        item["percentPositiveA"],
                        item["percentPositiveB"],
                        item["percentPositive"]
                    )
                )
            )

        return USCL(
            updated,
            source,
            weeks
        )


    async def usphl(self) -> USPHL:
        """
        Get Influenza report data for the 2019 and 2020 outbreaks from the US Center for Disease Control, reported by US public health labs
        """
        endpoint = FLU_USPHL.format(self.api_url)

        data = await self.request_client.make_request(endpoint)

        updated = datetime.utcfromtimestamp(data.get('updated')/1000)
        source = data.get('source')

        weeks = []
        for item in data["data"]:
            weeks.append(
                USPHLData(
                    item["week"],
                    TypeA(
                        item["A(H3N2v)"],
                        item["A(H1N1)"],
                        item["A(H3)"],
                        item["A(unable to sub-type)"],
                        item["A(Subtyping not performed)"]
                    ),
                    item["B"],
                    item["BVIC"],
                    item["BYAM"],
                    item["totalTests"]
                )

            )
        return USPHL(
            updated,
            source,
            weeks
        )