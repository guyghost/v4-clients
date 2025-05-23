from typing import List

from v4_proto.cosmos.bank.v1beta1.tx_pb2 import MsgSend
from v4_proto.cosmos.base.v1beta1.coin_pb2 import Coin
from v4_proto.dydxprotocol.clob.order_pb2 import Order, OrderId
from v4_proto.dydxprotocol.clob.tx_pb2 import MsgCancelOrder, MsgPlaceOrder
from v4_proto.dydxprotocol.sending.transfer_pb2 import (
    MsgDepositToSubaccount,
    MsgWithdrawFromSubaccount,
    Transfer,
)
from v4_proto.dydxprotocol.sending.tx_pb2 import MsgCreateTransfer
from v4_proto.dydxprotocol.subaccounts.subaccount_pb2 import SubaccountId
from v4_proto.dydxprotocol.clob.tx_pb2 import MsgBatchCancel, OrderBatch
from v4_proto.dydxprotocol.accountplus.tx_pb2 import (
    MsgAddAuthenticator,
    MsgRemoveAuthenticator,
)
import json
import base64

PY_V2_CLIENT_ID = 2


def order(
    order_id: OrderId,
    side: Order.Side,
    quantums: int,
    subticks: int,
    time_in_force: Order.TimeInForce,
    reduce_only: bool,
    good_til_block: int = None,
    good_til_block_time: int = None,
    client_metadata: int = 0,
    condition_type: Order.ConditionType = Order.ConditionType.CONDITION_TYPE_UNSPECIFIED,
    conditional_order_trigger_subticks: int = 0,
):
    return Order(
        order_id=order_id,
        side=side,
        quantums=quantums,
        subticks=subticks,
        good_til_block=good_til_block,
        good_til_block_time=good_til_block_time,
        time_in_force=time_in_force,
        reduce_only=reduce_only,
        client_metadata=PY_V2_CLIENT_ID,
        condition_type=condition_type,
        conditional_order_trigger_subticks=conditional_order_trigger_subticks,
    )


def order_id(
    address: str,
    subaccount_number: int,
    client_id: int,
    clob_pair_id: int,
    order_flags: int,
) -> OrderId:
    return OrderId(
        subaccount_id=subaccount(owner=address, number=subaccount_number),
        client_id=client_id,
        order_flags=order_flags,
        clob_pair_id=clob_pair_id,
    )


def subaccount(owner: str, number: int):
    return SubaccountId(owner=owner, number=number)


def place_order(order: Order):
    return MsgPlaceOrder(order=order)


def cancel_order(
    order_id: OrderId,
    good_til_block: int = None,
    good_til_block_time: int = None,
):
    message = MsgCancelOrder(
        order_id=order_id,
        good_til_block=good_til_block,
        good_til_block_time=good_til_block_time,
    )
    return message


def batch_cancel(
    subaccount_id: SubaccountId,
    short_term_cancels: List[OrderBatch],
    good_til_block: int,
):
    message = MsgBatchCancel(
        subaccount_id=subaccount_id,
        short_term_cancels=short_term_cancels,
        good_til_block=good_til_block,
    )
    return message


def transfer(
    sender_subaccount: SubaccountId,
    recipient_subaccount: SubaccountId,
    asset_id: int,
    amount: int,
):

    msg = Transfer(
        sender=sender_subaccount,
        recipient=recipient_subaccount,
        asset_id=asset_id,
        amount=amount,
    )

    return MsgCreateTransfer(transfer=msg)


def deposit(
    sender: str,
    recipient_subaccount: SubaccountId,
    asset_id: int,
    quantums: int,
):
    message = MsgDepositToSubaccount(
        sender=sender,
        recipient=recipient_subaccount,
        asset_id=asset_id,
        quantums=quantums,
    )
    return message


def withdraw(
    sender_subaccount: SubaccountId,
    recipient: str,
    asset_id: int,
    quantums: int,
):
    message = MsgWithdrawFromSubaccount(
        sender=sender_subaccount,
        recipient=recipient,
        asset_id=asset_id,
        quantums=quantums,
    )
    return message


def send_token(sender: str, recipient: str, quantums: int, denomination: str):
    message = MsgSend(
        from_address=sender,
        to_address=recipient,
        amount=[Coin(amount=str(quantums), denom=denomination)],
    )
    return message


def add_authenticator(sender: str, auth_type: str, config: bytes):
    message = MsgAddAuthenticator(
        sender=sender,
        authenticator_type=auth_type,
        data=convert_nested_config_to_base64(config),
    )
    return message


def remove_authenticator(sender: str, authenticator_id: int):
    message = MsgRemoveAuthenticator(
        sender=sender,
        id=authenticator_id,
    )
    return message


def convert_nested_config_to_base64(config: bytes):
    try:
        config_json_array = json.loads(config.decode())
        for config_json in config_json_array:
            if config_json["type"] == "AnyOf" or config_json["type"] == "AllOf":
                config_json["config"] = convert_nested_config_to_base64(
                    bytes(config_json["config"])
                )
            config_json["config"] = base64.b64encode(
                bytes(config_json["config"])
            ).decode()
        config_modified = json.dumps(config_json_array)
        return config_modified.encode()
    except:
        return config
