from random import randint
from faker import Faker


def create_fake_data(amount: int) -> list:
    return [
        {
            "total_fat": f'{randint(1, 100)} g',
            "cholesterol": f'{randint(1, 100)} mg',
            "sodium": f'{randint(1, 500)} mg',
            "potassium": f'{randint(1, 300)} mg',
            "total_carbohydrate": f'{randint(1, 100)} g',
            "protein": f'{randint(1, 100)} g',
            "user_id": randint(1, 999999999),
            # date example: 2025-03-03T16:05:27.863+00:00
            "date": f'{randint(2020, 2025)}-{randint(1, 12)}-{randint(1, 28)}'
                    f'T{randint(0, 23)}:{randint(0, 59)}:{randint(0, 59)}'
                    f'.{randint(0, 999)}+00:00',
            "name": Faker().name()
        }
        for i in range(amount)
    ]
