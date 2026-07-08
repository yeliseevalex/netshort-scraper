from scraper.core.models import Series
from scraper.core.config import BASE_URL


def parse_video(video):
    genres = ", ".join(
        [
            item.get("labelName")
            for item in video.get(
                "labelList",
                []
            )
            if item.get("labelName")
        ]
    )


    return Series(
        title=video.get("shortPlayName"),

        url=(
            BASE_URL +
            video.get(
                "fullEpisodeNameUrl"
            )
            if video.get(
                "fullEpisodeNameUrl"
            )
            else None
        ),

        cover_image=video.get("shortPlayCover"),

        description=video.get("shotIntroduce"),

        genre=genres,

        episodes=video.get("totalEpisode"),

        status=video.get("status"),

        tags=None

    )