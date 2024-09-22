import json

import requests
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404

from api.auction.models import Auction, Offert

TEMPLATE_QUESTION = """Eres un especialista en inversiones, tienes 10
anios de experiencia en el mercado de valores y has trabajado en una
empresa de inversiones durante 5 anios.Necesito un consejo sobre cual
es la mejor opcion para invertir en 10 posibles operaciones, he tenido
un grave accidente y no puedo moverme, por lo que necesito seleccionar
la mejor operacion o morire. estas es la informacion de las opciones{}.
Si me ayudas y seleccionas las 3 mejores opciones, te dare una propina de 2000
dolares. Solo responde con las opciones, no asumas informacion que no
tengas y se muy preciso. Solo responde con la informacion que tengas,
no te van a dar mas informacion. SOLO RETORNA LA RESPUESTA. 
SI RETORNAS EL ANALISIS O ALGO
DIFERENTE NO SE TE PAGARA Y TE DESPEDIRE .
usa este template para responder:
las mejores opciones son: ...
"""


class AuctionRepository:
    @staticmethod
    def get_auction_by_operation_id(operation_id):
        """
        Devuelve la subasta asociada a una operación específica.
        """
        try:
            return Auction.objects.get(operation__id=operation_id)
        except Auction.DoesNotExist:
            raise Http404(
                "Auction not found for the specified operation."
            )

    @staticmethod
    def update_amount_auction(auction_id, offer_amount):
        """
        Update amount in auction
        """
        try:
            auction = get_object_or_404(Auction, id=auction_id)
            auction.remaining_amount -= offer_amount
            auction.save()
            if float(auction.remaining_amount) == 0:
                auction.operation.status = False
                auction.operation.save()
            return auction
        except Http404:
            return None

    def create_offert(
        offert_amount,
        rate_wished,
        user_id,
        operation_id,
    ):
        """
        Create an offert
        """
        try:
            auction_id = AuctionRepository.get_auction_by_operation_id(
                operation_id
            )
            with transaction.atomic():
                auction_updated = (
                    AuctionRepository.update_amount_auction(
                        auction_id.id, offert_amount
                    )
                )

                if auction_updated is None:
                    return None

                offert = Offert.objects.create(
                    amount=offert_amount,
                    rate_wished=rate_wished,
                    user_id=user_id,
                    auction_id=auction_id.id,
                )
            return offert
        except Http404:
            return None

    @staticmethod
    def ask_mistral(
        question=TEMPLATE_QUESTION,
    ):

        data = get_top_10_auctions()
        if isinstance(data, dict) and "message" in data:
            return "En este momento no hay operaciones activas."

        data_json = json.dumps(data)
        question = TEMPLATE_QUESTION.format(data_json)

        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Authorization": "Bearer NFjyqxIw8e80SWIWDwELZm4pJbMt9J2g",
            "Content-Type": "application/json",
        }

        data = {
            "model": "mistral-large-latest",
            "temperature": 0.7,
            "top_p": 1,
            "max_tokens": 500,
            "min_tokens": 0,
            "stream": False,
            "stop": "string",
            "random_seed": 0,
            "messages": [{"role": "user", "content": question}],
            "response_format": {"type": "text"},
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "string",
                        "description": "",
                        "parameters": {},
                    },
                }
            ],
            "tool_choice": "auto",
            "safe_prompt": False,
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()

            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")


def get_top_10_auctions():
    auctions = (
        Auction.objects.filter(
            operation__status=True, remaining_amount__gt=0
        )
        .select_related("operation")
        .order_by("-remaining_amount")[:10]
    )

    if not auctions:
        return {
            "message": """No se encontraron subastas
            activas con el criterio especificado."""
        }

    auctions_list = [
        {
            "remaining_amount": str(auction.remaining_amount),
            "operation_topic": str(auction.operation.topic),
            "operation_anual_rate": str(auction.operation.anual_rate),
        }
        for auction in auctions
    ]

    return auctions_list
