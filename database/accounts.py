from database.base import *
from base64 import b64encode, b64decode

__all__ = [
    "create_guild_account",
    "add_account",
    "get_account",
    "ip_exists",
    "update_ip",
    "remove_account"
]


def create_guild_account(guild_id: int) -> None:
    name = f"g_{guild_id}"
    DB.run(
        f"CREATE TABLE IF NOT EXISTS `{name}`(user_id BIGINT PRIMARY KEY, ip VARCHAR(100))",
    )


def add_account(guild_id: int, user_id: int) -> None:
    name = f"g_{guild_id}"
    data = DB.execute(
        "SELECT * FROM " + f"`{name}`" + " WHERE user_id = %s",
        (user_id,), fetch="one"
    )
    if data is None:
        DB.run(
            "INSERT INTO " + f"`{name}`" + "(user_id) VALUES(%s)",
            (user_id,)
        )


def get_account(guild_id: int, user_id: int) -> RowSet:
    name = f"g_{guild_id}"
    rows = DB.execute(
        f"SELECT * FROM " + f"`{name}`" + " WHERE user_id = %s",
        (user_id,), fetch="one"
    )

    data = [_ for _ in rows]
    if data[1] is not None:
        data[1] = b64decode(data[1]).decode()

    return tuple(data)


def ip_exists(guild_id: int, ip: str) -> bool:
    name = f"g_{guild_id}"
    ip = b64encode(ip.encode()).decode()
    data = DB.execute(
        "SELECT * FROM " + f"`{name}`" + " WHERE ip = %s",
        (ip,), fetch="one"
    )

    return data is not None


def update_ip(guild_id: int, user_id: int, ip: str | None) -> None:
    name = f"g_{guild_id}"
    if ip is not None:
        ip = b64encode(ip.encode()).decode()

    data = DB.execute(
        "SELECT * FROM " + f"`{name}`" + " WHERE user_id = %s",
        (user_id,), fetch="one"
    )
    if data is not None:
        DB.run(
            "UPDATE " + f"`{name}`" + " SET ip = %s WHERE user_id = %s",
            (ip, user_id)
        )


def remove_account(guild_id: int, user_id: int) -> None:
    name = f"g_{guild_id}"
    DB.run(
        "DELETE FROM " + f"`{name}`" + " WHERE user_id = %s",
        (user_id,)
    )
