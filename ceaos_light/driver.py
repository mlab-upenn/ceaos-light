import time
import json
import zmq
from apogee import Quantum


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://158.130.113.109:23267")
    time.sleep(2)
    light = Quantum()

    while True:
        payload = json.dumps(
            {
                "action": "recv_value",
                "cea-addr": "farm1.env1.bed1.light1",
                "payload": {
                    "light": light.get_micromoles()
                },
            }
        )
        socket.send_string(payload)
        reply = socket.recv()
        reply = json.loads(reply)
        print(reply)
        time.sleep(600)

if __name__ == '__main__':
    main()