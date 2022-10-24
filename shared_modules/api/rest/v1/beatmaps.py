from shared_modules import logger
from shared_modules.http_client import ServiceHTTPClient
from shared_modules.models.beatmaps import Beatmap
from shared_modules.models.beatmapsets import Beatmapset

SERVICE_URL = "http://beatmaps-service"


class BeatmapsClient:
    def __init__(self, http_client: ServiceHTTPClient) -> None:
        self.http_client = http_client

    # beatmaps

    async def get_beatmap(self, beatmap_id: int) -> Beatmap | None:
        response = await self.http_client.service_call(
            method="GET",
            url=f"{SERVICE_URL}/v1/beatmaps/{beatmap_id}",
        )
        if response.status_code not in range(200, 300):
            logger.error("Failed to get beatmap",
                         status=response.status_code,
                         response=response.json)
            return None

        return Beatmap(**response.json['data'])

    async def get_beatmaps(self, set_id: int | None = None,
                           md5_hash: str | None = None,
                           mode: str | None = None,
                           ranked_status: int | None = None,
                           status: str | None = None,
                           page: int = 1,
                           page_size: int = 20,
                           ) -> list[Beatmap] | None:
        response = await self.http_client.service_call(
            method="GET",
            url=f"{SERVICE_URL}/v1/beatmaps",
            params={
                "set_id": set_id,
                "md5_hash": md5_hash,
                "mode": mode,
                "ranked_status": ranked_status,
                "status": status,
                "page": page,
                "page_size": page_size,
            })
        if response.status_code not in range(200, 300):
            logger.error("Failed to get beatmaps",
                         status=response.status_code,
                         response=response.json)
            return None

        return [Beatmap(**rec) for rec in response.json['data']]

    # beatmapsets

    async def get_beatmapset(self, set_id: int) -> Beatmapset | None:
        response = await self.http_client.service_call(
            method="GET",
            url=f"{SERVICE_URL}/v1/beatmapsets/{set_id}",
        )
        if response.status_code not in range(200, 300):
            logger.error("Failed to get beatmapset",
                         status=response.status_code,
                         response=response.json)
            return None

        return Beatmapset(**response.json['data'])

    async def get_beatmapsets(self, set_id: int | None = None,
                              artist: str | None = None,
                              creator: str | None = None,
                              title: str | None = None,
                              nsfw: bool | None = None,
                              ranked_status: int | None = None,
                              status: str | None = None,
                              page: int = 1,
                              page_size: int = 20,
                              ) -> list[Beatmapset] | None:
        response = await self.http_client.service_call(
            method="GET",
            url=f"{SERVICE_URL}/v1/beatmapsets",
            params={
                "set_id": set_id,
                "artist": artist,
                "creator": creator,
                "title": title,
                "nsfw": nsfw,
                "ranked_status": ranked_status,
                "status":  status,
                "page": page,
                "page_size": page_size,
            },
        )
        if response.status_code not in range(200, 300):
            logger.error("Failed to get beatmapsets",
                         status=response.status_code,
                         response=response.json)
            return None

        return [Beatmapset(**rec) for rec in response.json['data']]
