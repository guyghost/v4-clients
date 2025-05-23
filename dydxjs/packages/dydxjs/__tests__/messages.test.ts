import { cosmos } from '../src';
import { assertEquals } from "https://deno.land/std@0.106.0/testing/asserts.ts";

Deno.test('cosmos', () => {
    const message = cosmos.bank.v1beta1.MessageComposer.fromPartial.send({
        amount: [
            {
                amount: '1',
                denom: 'uatom'
            }
        ],
        fromAddress: 'myaddress',
        toAddress: 'youraddress'
    });
    assertEquals(message, {
        typeUrl: "/cosmos.bank.v1beta1.MsgSend",
        value: {
            fromAddress: "myaddress",
            toAddress: "youraddress",
            amount: [
                {
                    denom: "uatom",
                    amount: "1"
                }
            ]
        }
    });
});
