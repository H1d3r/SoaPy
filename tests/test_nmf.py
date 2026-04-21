import unittest

from hypothesis import given
from hypothesis.strategies import integers, text, binary

from src.ms_nmf import (
    NMFConnection,
    NMFRecord,
    NMFVersion,
    NMFMode,
    NMFVia,
    NMFKnownEncoding,
    NMFSizedEnvelope,
    NMFEnd,
    NMFFault,
    NMFUpgradeRequest,
    NMFUpgradeResponse,
    NMFPreambleEnd,
    NMFPreambleAck,
    NMFPreamble,
    ) 


class DummyTransport:
    def __init__(self, chunks):
        self._chunks = list(chunks)
        self._sock = object()

    def recv(self, _: int = 0) -> bytes:
        return self._chunks.pop(0) if self._chunks else b""

    def sendall(self, _: bytes) -> None:
        return None


class TestSizeEncoding(unittest.TestCase):
    """Testing the variable length field encoding of 
    [MC-NMF] record sizes.

    The record size feild (payload len) is variable between
    1 and 5 bytes.  Or between 0x0 and 0xFFFFFFFF
    """


    def test_decode_simple(self):

        expected_size = 0x92
        data = b'\x92\01'

        size, _, _ = NMFRecord.decode_size(data)
        self.assertEqual(size, expected_size)
    
    def test_decode_three(self):
        data = b'\x80\x81\x01'
        expected_size = 0x4080

        size, _, _ = NMFRecord.decode_size(data)
        self.assertEqual(size, expected_size)
    
    def test_decode_16(self):
        data = b'\x10'
        expected_size = 0x10

        size, _, _ = NMFRecord.decode_size(data)
        self.assertEqual(size, expected_size)

    # ======= Encode Tests =========
    
    def test_encode_simple(self):

        expected_data = b'\x92\01'
        size = 0x92

        data = NMFRecord.encode_size(size)
        self.assertEqual(data, expected_data)
    

    def test_encode_three_bytes(self):

        expected_data = b'\x80\x81\x01'
        size = 0x4080

        data = NMFRecord.encode_size(size)
        self.assertEqual(data, expected_data)


    def test_encode_16(self):

        expected_data = b'\x10'
        size = 0x10

        data = NMFRecord.encode_size(size)
        self.assertEqual(data, expected_data)

    # stress test

    @given(integers(min_value=0x0, max_value=0xFFFFFFFF))
    def test_decoding_invariant(self, i):
        self.assertEqual(NMFRecord.decode_size(NMFRecord.encode_size(i))[0], i)


class TestRecords(unittest.TestCase):


    @given(v1=integers(min_value=0x0, max_value=0xff), v2=integers(min_value=0x0, max_value=0xff))
    def test_version_record_invariant(self, v1, v2):
        data = NMFVersion(minor_version=v1, major_version=v2).getData()
        v = NMFVersion(data=data)
        self.assertEqual(v['major_version'], v2)
        self.assertEqual(v['minor_version'], v1)
    
    @given(i=integers(min_value=0x0, max_value=0x4))
    def test_mode_record_invariants(self, i):
        data = NMFMode(mode=i).getData()
        v = NMFMode(data=data)
        self.assertEqual(v['mode'], i)

    @given(s=text(max_size=0xFFFFFFFF))
    def test_via_record_invaiant(self, s):
        data = NMFVia(s).getData()
        v = NMFVia(data=data)
        self.assertEqual(v['via'], s)
    
    @given(i=integers(min_value=0x0, max_value=0xff))
    def test_knownencoding_record_invariant(self, i):
        data = NMFKnownEncoding(i).getData()
        v = NMFKnownEncoding(data=data)
        self.assertEqual(v['encoding'], i)

    @given(b=binary(max_size=0xffffffff))
    def test_sizedenvelope_invaiant(self, b):
        data = NMFSizedEnvelope(b).getData()
        v = NMFSizedEnvelope(data=data)
        self.assertEqual(v['payload'], b)
    
    def test_end_record(self):
        data = NMFEnd().getData()
        v = NMFEnd(data=data)
        self.assertEqual(v['record_type'], 0x7)

    @given(s=text(max_size=0xFFFFFFFF))
    def test_fault_record_invaiant(self, s):
        data = NMFFault(s).getData()
        v = NMFFault(data=data)
        self.assertEqual(v['fault'], s)
    
    @given(s=text(max_size=0xffffffff))
    def test_upgrade_request_record_invariant(self, s):
        data = NMFUpgradeRequest(s).getData()
        v = NMFUpgradeRequest(data=data)
        self.assertEqual(v['proto'], s)

    def test_upgrade_response_record(self):
        data = NMFUpgradeResponse().getData()
        v = NMFUpgradeResponse(data=data)
        self.assertEqual(v['record_type'], 0xA)
    
    def test_preamble_end_record(self):
        data = NMFPreambleEnd().getData()
        v = NMFPreambleEnd(data=data)
        self.assertEqual(v['record_type'], 0xC)

    def test_preamble_ack_record(self):
        data = NMFPreambleAck().getData()
        v = NMFPreambleAck(data=data)
        self.assertEqual(v['record_type'], 0xB)

    def test_preamble_record(self):
        version = (1, 1)
        mode = 0x1
        via = "test_via"
        encoding = 0x4
        data = NMFPreamble(version, mode, via, encoding).getData()
        expected = NMFVersion(*version).getData()
        expected += NMFMode(mode).getData()
        expected += NMFVia(via).getData()
        expected += NMFKnownEncoding(encoding).getData()
        self.assertEqual(data, expected)

    def test_recv_buffers_fragmented_records(self):
        payload = b"<xml>" * 2000
        envelope = NMFSizedEnvelope(payload).getData()
        end_record = NMFEnd().getData()
        transport = DummyTransport(
            [
                envelope[:11],
                envelope[11:257],
                envelope[257:] + end_record,
            ]
        )
        conn = NMFConnection(transport, fqdn="dc.example.com")
        conn._transport = transport

        pkt = conn._recv()
        self.assertEqual(pkt["payload"], payload)

        pkt = conn._recv()
        self.assertEqual(pkt["record_type"], 0x7)
