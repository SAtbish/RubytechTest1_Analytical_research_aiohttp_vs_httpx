"""
Тестовое задание №1 - аналитическая работа (ориентировочное время выполнения - 2 часа)
Нужно найти и проанализировать несколько Python-библиотек, специализирующихся на асинхронных запросах к внешним
источникам в интернете. Библиотека должна помочь регулярно опрашивать статус коды ответа ста тысяч сайтов за
минимальное время, при этом не попасть под блокировку со стороны хостинга и с минимальным потреблением CPU и RAM.
Предоставить отчет в виде таблицы, с описанием основных характеристик, плюсов и минусов каждой из библиотек.
В последней строчке таблицы должен содержаться общий вывод - какую из библиотек вы бы выбрали для использования
и почему.
"""

import asyncio
import json
import time

import aiohttp
import httpx

from logger.logger import create_logger

logger = create_logger(__name__)

f = open("urls.json")
URLS = json.load(f)["urls"]
f.close()

COUNT_OF_REQUESTS = (
    100  # такое маленькое количество, т.к. некоторые api начинают кидать 429 статус.
)


async def main():
    timeouts = [3, 5]
    connections = [100 * i for i in range(2, 11, 2)]
    for url in URLS:
        aiohttp_total_time = 0
        httpx_total_time = 0
        logger.info(f"\n\nНачинается тестирование запросов по ссылке {url}.")
        for timeout in timeouts:
            for connection in connections:
                httpx_client = httpx.AsyncClient(
                    limits=httpx.Limits(max_connections=connection)
                )
                aiohttp_client = aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(limit=connection)
                )
                logger.info(f"(httpx) Количество подключений = {connection}.")
                logger.info(f"(httpx) Таймаут = {timeout}.")
                logger.info(
                    f"(httpx) Начинается отправка {COUNT_OF_REQUESTS} асинхронных запросов с помощью httpx."
                )
                httpx_start_time = time.perf_counter()
                httpx_tasks = [
                    httpx_client.get(url, timeout=timeout)
                    for _ in range(COUNT_OF_REQUESTS)
                ]
                httpx_results = await asyncio.gather(
                    *httpx_tasks, return_exceptions=True
                )
                httpx_end_time = time.perf_counter()
                httpx_result_dict = {"Timeout_Errors": 0}
                for result in httpx_results:
                    if isinstance(result, Exception):
                        httpx_result_dict["Timeout_Errors"] += 1
                    else:
                        if (status := result.status_code) not in httpx_result_dict:
                            httpx_result_dict[status] = 1
                        else:
                            httpx_result_dict[status] += 1
                httpx_final_time = httpx_end_time - httpx_start_time
                logger.info(f"(httpx) Статистика ответов: {httpx_result_dict}.")
                logger.info(
                    f"(httpx) Было выполнено за {httpx_final_time:.2f} секунды."
                )

                logger.info(
                    f"(aiohttp) Начинается отправка {COUNT_OF_REQUESTS} асинхронных запросов с помощью aiohttp."
                )
                aiohttp_start_time = time.perf_counter()
                aiohttp_tasks = [
                    aiohttp_client.get(url, timeout=timeout)
                    for _ in range(COUNT_OF_REQUESTS)
                ]
                aiohttp_results = await asyncio.gather(
                    *aiohttp_tasks, return_exceptions=True
                )
                aiohttp_end_time = time.perf_counter()
                aiohttp_result_dict = {"Timeout_Errors": 0}
                for result in aiohttp_results:
                    if isinstance(result, Exception):
                        aiohttp_result_dict["Timeout_Errors"] += 1
                    else:
                        if (status := result.status) not in aiohttp_result_dict:
                            aiohttp_result_dict[status] = 1
                        else:
                            aiohttp_result_dict[status] += 1
                aiohttp_final_time = aiohttp_end_time - aiohttp_start_time
                logger.info(f"(aiohttp) Статистика ответов: {aiohttp_result_dict}.")
                logger.info(
                    f"(aiohttp) Было выполнено за {aiohttp_final_time:.2f} секунды."
                )
                if aiohttp_final_time < httpx_final_time:
                    logger.info(
                        f"Aiohttp выполнил запросы быстрее на {httpx_final_time - aiohttp_final_time:2f} секунд."
                    )
                else:
                    logger.info(
                        f"Httpx выполнил запросы быстрее на {aiohttp_final_time - httpx_final_time:2f} секунд."
                    )
                aiohttp_total_time += aiohttp_final_time
                httpx_total_time += httpx_final_time
                await aiohttp_client.close()
                await httpx_client.aclose()
                logger.info(
                    f"Тестирование ссылки {url} с таймаутом = {timeout} и подключениями = {connection} завершено.\n"
                )

        logger.info(
            f"Тестирование запросов по ссылке {url} завершено."
            f"Время выполнения всех запросов с aiohttp = {aiohttp_total_time:2f}."
            f"Время выполнения всех запросов с httpx = {httpx_total_time:2f}."
            f"Разница между библиотеками = {abs(httpx_total_time - aiohttp_total_time):2f}."
        )


asyncio.run(main())
