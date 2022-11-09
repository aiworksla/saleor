from ....core.permissions import DiscountPermissions
from ....core.tracing import traced_atomic_transaction
from ....discount.utils import fetch_catalogue_info
from ...channel import ChannelContext
from ...core.types import DiscountError
from ...plugins.dataloaders import load_plugin_manager
from ..types import Sale
from .sale_base_catalogue import SaleBaseCatalogueMutation
from .utils import convert_catalogue_info_to_global_ids


class SaleAddCatalogues(SaleBaseCatalogueMutation):
    class Meta:
        description = "Adds products, categories, collections to a voucher."
        permissions = (DiscountPermissions.MANAGE_DISCOUNTS,)
        error_type_class = DiscountError
        error_type_field = "discount_errors"

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        sale = cls.get_node_or_error(
            info, data.get("id"), only_type=Sale, field="sale_id"
        )
        previous_catalogue = fetch_catalogue_info(sale)
        manager = load_plugin_manager(info.context)
        with traced_atomic_transaction():
            cls.add_catalogues_to_node(sale, data.get("input"))
            current_catalogue = fetch_catalogue_info(sale)
            previous_cat_converted = convert_catalogue_info_to_global_ids(
                previous_catalogue
            )
            current_cat_converted = convert_catalogue_info_to_global_ids(
                current_catalogue
            )

            def sale_update_event():
                return manager.sale_updated(
                    sale,
                    previous_catalogue=previous_cat_converted,
                    current_catalogue=current_cat_converted,
                )

            cls.call_event(sale_update_event)

        return SaleAddCatalogues(sale=ChannelContext(node=sale, channel_slug=None))
