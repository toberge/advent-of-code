from typing import List

LITERAL_TYPE = 0b100


class Packet:
    def __init__(self, version: int):
        self.version = version


class LiteralPacket(Packet):
    def __init__(self, version: int, value: int):
        super().__init__(version)
        self.value = value


class OperatorPacket(Packet):
    def __init__(self, version: int, packets: List[Packet]):
        super().__init__(version)
        self.packets = packets


def extract(byte, amount, start):
    amount = min(amount, 8 - start)
    remainder = 8 - amount - start
    return (byte & (((1 << amount) - 1) << remainder)) >> remainder


class BitStream:
    def __init__(self, hex_string):
        self.stream = (
            int(hex_string[i : i + 2], base=16) for i in range(0, len(hex_string), 2)
        )
        self.byte = next(self.stream)
        self.pos = 0
        self.bits_read = 0

    def read_number(self, n=1):
        num = 0
        i = 0
        pos = self.pos
        self.bits_read += n

        # Read last/middle part of byte
        i += min(8 - pos, n)
        num = extract(self.byte, n, pos)
        pos += i
        if pos >= 8:
            pos = 0
            self.byte = next(self.stream)

        while i < n:
            if n - i > 8:
                # Read an entire byte
                i += 8
                num = (num << 8) + self.byte
                self.byte = next(self.stream)
                pos = 0
            else:
                # Read first part of byte
                rem = n - i
                i += rem
                pos += rem
                num = (num << rem) + extract(self.byte, rem, 0)

        self.pos = pos

        return num

    def read_packet(self):
        # read header
        version = self.read_number(3)
        type_id = self.read_number(3)
        # read whatever comes next
        if type_id == LITERAL_TYPE:
            return self.read_literal(version)
        else:
            return self.read_operator(version)

    def read_operator(self, version: int):
        length_type = self.read_number()
        if length_type == 1:
            # number of subpackets
            length = self.read_number(11)
            packets = [self.read_packet() for _ in range(length)]
        else:
            # number of bits with subpackets
            length = self.read_number(15)
            packets = []
            start = self.bits_read
            while self.bits_read < start + length:
                packets.append(self.read_packet())
        return OperatorPacket(version, packets)

    def read_literal(self, version: int):
        leading_bit = 1
        value = 0
        while leading_bit == 1:
            leading_bit = self.read_number()
            value = (value << 4) + self.read_number(4)
        return LiteralPacket(version, value)


def version_sum(packet: Packet):
    if isinstance(packet, LiteralPacket):
        return packet.version
    elif isinstance(packet, OperatorPacket):
        return packet.version + sum(version_sum(p) for p in packet.packets)


def main():
    hex_string = input()
    stream = BitStream(hex_string)

    root_packet = stream.read_packet()
    print("Part 1:", version_sum(root_packet))


if __name__ == "__main__":
    main()
