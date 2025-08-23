import threading
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import Callable

PRECISION = 1000


class Cost(int):
    @property
    def whole_num_part(self) -> int:
        return self // PRECISION

    @property
    def fraction_part(self) -> int:
        return self % PRECISION


@dataclass(frozen=True)
class BankDetails:
    bank_name: str
    ifsc_code: str
    account_number: str


class PaymentStatus(Enum):
    SUCCESS = "SUCCESS"
    PENDING = "PENDING"
    FAILURE = "FAILURE"


class IPayment(ABC):
    def request(
        self,
        cost: Cost,
        bank_details: BankDetails,
        callback: Callable[[PaymentStatus], None]
    ) -> None:
        raise NotImplementedError()


class DummyPaymentManager(IPayment):
    def request(
        self,
        cost: Cost,
        bank_details: BankDetails,
        callback: Callable[[PaymentStatus], None]
    ) -> None:

        def _payment():
            import time
            time.sleep(1.0)
            callback(PaymentStatus.SUCCESS)

        thread = threading.Thread(target=_payment, args=())
        thread.start()
        return


def get_bank_details():
    return BankDetails(
        bank_name="Some Bank",
        ifsc_code="some00001",
        account_number="abc0001"
    )
