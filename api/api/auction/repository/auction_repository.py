from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404

from api.auction.models import Auction, Offert


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
