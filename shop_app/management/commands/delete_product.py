from django.core.management.base import BaseCommand
from shop_app.models import Product
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Удалить товар по ID"

    def add_arguments(self, parser):
        parser.add_argument('pk', type=int, help='ID товара')

    def handle(self, *args, **kwargs):
        pk = kwargs['pk']
        product = Product.objects.filter(pk=pk).first()
        if product is not None:
            product.delete()
        self.stdout.write(f'{product}')
        logger.info(f'Товар {product} удален')
