# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: header.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='header.proto',
  package='pb',
  syntax='proto3',
  serialized_pb=_b('\n\x0cheader.proto\x12\x02pb\"\xd2\x02\n\x06Header\x12\x11\n\ttimestamp\x18\x01 \x01(\x03\x12\x34\n\x10timestamp_source\x18\x02 \x01(\x0e\x32\x1a.pb.Header.TimeStampSource\x12;\n\x14timestamp_sync_state\x18\x03 \x01(\x0e\x32\x1d.pb.Header.TimeStampSyncState\x12\x1a\n\x12timestamp_calendar\x18\x04 \x01(\t\";\n\x0fTimeStampSource\x12\x12\n\x0eUNKNOWN_SOURCE\x10\x00\x12\n\n\x06SENSOR\x10\x01\x12\x08\n\x04\x41LGO\x10\x02\"i\n\x12TimeStampSyncState\x12\x10\n\x0cUNKNOWN_SYNC\x10\x00\x12\x0e\n\nNOT_SYNCED\x10\x01\x12\x0e\n\nSYNCED_GTC\x10\x02\x12\x0e\n\nSYNCED_PTP\x10\x03\x12\x11\n\rSYNCED_REPLAY\x10\x04\x42\x0b\x42\tMsgHeaderb\x06proto3')
)



_HEADER_TIMESTAMPSOURCE = _descriptor.EnumDescriptor(
  name='TimeStampSource',
  full_name='pb.Header.TimeStampSource',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_SOURCE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SENSOR', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ALGO', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=193,
  serialized_end=252,
)
_sym_db.RegisterEnumDescriptor(_HEADER_TIMESTAMPSOURCE)

_HEADER_TIMESTAMPSYNCSTATE = _descriptor.EnumDescriptor(
  name='TimeStampSyncState',
  full_name='pb.Header.TimeStampSyncState',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_SYNC', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NOT_SYNCED', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SYNCED_GTC', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SYNCED_PTP', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SYNCED_REPLAY', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=254,
  serialized_end=359,
)
_sym_db.RegisterEnumDescriptor(_HEADER_TIMESTAMPSYNCSTATE)


_HEADER = _descriptor.Descriptor(
  name='Header',
  full_name='pb.Header',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='pb.Header.timestamp', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_source', full_name='pb.Header.timestamp_source', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_sync_state', full_name='pb.Header.timestamp_sync_state', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_calendar', full_name='pb.Header.timestamp_calendar', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _HEADER_TIMESTAMPSOURCE,
    _HEADER_TIMESTAMPSYNCSTATE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=21,
  serialized_end=359,
)

_HEADER.fields_by_name['timestamp_source'].enum_type = _HEADER_TIMESTAMPSOURCE
_HEADER.fields_by_name['timestamp_sync_state'].enum_type = _HEADER_TIMESTAMPSYNCSTATE
_HEADER_TIMESTAMPSOURCE.containing_type = _HEADER
_HEADER_TIMESTAMPSYNCSTATE.containing_type = _HEADER
DESCRIPTOR.message_types_by_name['Header'] = _HEADER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Header = _reflection.GeneratedProtocolMessageType('Header', (_message.Message,), dict(
  DESCRIPTOR = _HEADER,
  __module__ = 'header_pb2'
  # @@protoc_insertion_point(class_scope:pb.Header)
  ))
_sym_db.RegisterMessage(Header)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\tMsgHeader'))
# @@protoc_insertion_point(module_scope)
