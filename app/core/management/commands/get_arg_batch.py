from django.core.management.base import BaseCommand


class Command(BaseCommand):
    # [python manage.py help sampleBatch]で表示されるメッセージ
    help = 'これはテスト用のコマンドバッチです'

    def add_arguments(self, parser):
        # コマンドライン引数を指定
        parser.add_argument(
            '-t',
            action='store',
            dest='intValue',
            help='',
            required=True,
            )

    def handle(self, *args, **options):
        try:
            print('バッチが動きました： {}'.format(options['intValue']))
        except Exception as e:
            print(e)


# def valid_type(t):
#     """
#     引数のバリデーション
#     :param unicode t:
#     :rtype: int
#     """
#     try:
#         product_type = int(t)
#         if product_type in [1, 2, 3, 4]:
#             return product_type
#         raise argparse.ArgumentTypeError('Choices a\
# re 1, 2, 3, 4 but {0} are given'.format(product_type))
#     except ValueError:
#         raise argparse.ArgumentTypeError('Not a valid type: {}.'.format(t))
