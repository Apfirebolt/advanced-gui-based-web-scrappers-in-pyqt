import aiohttp
import asyncio


async def main():

    async with aiohttp.ClientSession() as session:

        pokemon_url = 'https://pokeapi.co/api/v2/pokemon/151'
        print('Before..')
        async with session.get(pokemon_url) as resp:
            pokemon = await resp.json()
            print('After..')
            print(pokemon['name'], pokemon)

asyncio.run(main())