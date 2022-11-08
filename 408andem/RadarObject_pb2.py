# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: RadarObject.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import header_pb2 as header__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='RadarObject.proto',
  package='pb.ObjectLists',
  syntax='proto2',
  serialized_pb=_b('\n\x11RadarObject.proto\x12\x0epb.ObjectLists\x1a\x0cheader.proto\"\x82\t\n\x0fRadarObjectData\x12\x19\n\x0eobj_roll_count\x18\x01 \x01(\x11:\x01\x30\x12\x11\n\x06obj_id\x18\x02 \x01(\x11:\x01\x30\x12\x1b\n\x10obj_long_displ_m\x18\x03 \x01(\x02:\x01\x30\x12\x1b\n\x10obj_vrel_long_ms\x18\x04 \x01(\x02:\x01\x30\x12\x1d\n\x12obj_accel_long_ms2\x18\x05 \x01(\x02:\x01\x30\x12\x1c\n\x11obj_prob_of_exist\x18\x06 \x01(\x11:\x01\x30\x12\x17\n\x0cobj_dyn_prob\x18\x07 \x01(\x11:\x01\x30\x12\x1a\n\x0fobj_lat_displ_m\x18\x08 \x01(\x02:\x01\x30\x12\x15\n\nobj_length\x18\t \x01(\x11:\x01\x30\x12\x14\n\tobj_width\x18\n \x01(\x11:\x01\x30\x12\x18\n\robj_meas_stat\x18\x0b \x01(\x11:\x01\x30\x12\x1e\n\x13obj_rcs_value_d_bm2\x18\x0c \x01(\x02:\x01\x30\x12\x1b\n\x10obj_lat_speed_ms\x18\r \x01(\x02:\x01\x30\x12#\n\x18obj_obstacle_probability\x18\x0e \x01(\x11:\x01\x30\x12\x1f\n\x0bobj_f_width\x18\x0f \x01(\x02:\n1.66666663\x12\x1a\n\x0fobj_of_interest\x18\x10 \x01(\r:\x01\x30\x12K\n\x08obj_lane\x18\x11 \x01(\x0e\x32(.pb.ObjectLists.RadarObjectData.TObjLane:\x0fOBJLANE_UNKNOWN\x12N\n\tobj_class\x18\x12 \x01(\x0e\x32).pb.ObjectLists.RadarObjectData.TObjClass:\x10OBJCLASS_UNKONWN\x12\x1f\n\x14obj_long_displ_m_std\x18\x13 \x01(\x02:\x01\x30\x12\x1e\n\x13obj_lat_displ_m_std\x18\x14 \x01(\x02:\x01\x30\x12\x1f\n\x14obj_vrel_long_ms_std\x18\x15 \x01(\x02:\x01\x30\x12\x1f\n\x14obj_lat_speed_ms_std\x18\x16 \x01(\x02:\x01\x30\x12!\n\x16obj_accel_long_ms2_std\x18\x17 \x01(\x02:\x01\x30\"\x93\x01\n\x08TObjLane\x12\x1c\n\x0fOBJLANE_UNKNOWN\x10\x9d\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x1b\n\x0eOBJLANE_FAR_LT\x10\xfe\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x17\n\nOBJLANE_LT\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x0f\n\x0bOBJLANE_OWN\x10\x00\x12\x0e\n\nOBJLANE_RT\x10\x01\x12\x12\n\x0eOBJLANE_FAR_RT\x10\x02\"\xd5\x01\n\tTObjClass\x12\x14\n\x10OBJCLASS_UNKONWN\x10\x00\x12\x10\n\x0cOBJCLASS_CAR\x10\x01\x12\x12\n\x0eOBJCLASS_TRUCK\x10\x02\x12\x11\n\rOBJCLASS_BIKE\x10\x03\x12\x17\n\x13OBJCLASS_PEDESTRIAN\x10\x04\x12\x18\n\x14OBJCLASS_WIDE_OBJECT\x10\x05\x12\x19\n\x15OBJCLASS_POINT_OBJECT\x10\x06\x12\x13\n\x0fOBJCLASS_BRIDGE\x10\x07\x12\x16\n\x12OBJCLASS_GUARDRAIL\x10\x08\"?\n\x0bRadarStatus\x12\x16\n\x0eradar_CanRXErr\x18\x01 \x01(\x08\x12\x18\n\x10radar_HWFltPrsnt\x18\x02 \x01(\x08\"\x85\x01\n\x0bRadarObject\x12\x1a\n\x06header\x18\x01 \x01(\x0b\x32\n.pb.Header\x12-\n\x04\x64\x61ta\x18\x02 \x03(\x0b\x32\x1f.pb.ObjectLists.RadarObjectData\x12+\n\x06status\x18\x03 \x01(\x0b\x32\x1b.pb.ObjectLists.RadarStatus')
  ,
  dependencies=[header__pb2.DESCRIPTOR,])



_RADAROBJECTDATA_TOBJLANE = _descriptor.EnumDescriptor(
  name='TObjLane',
  full_name='pb.ObjectLists.RadarObjectData.TObjLane',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OBJLANE_UNKNOWN', index=0, number=-99,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OBJLANE_FAR_LT', index=1, number=-2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OBJLANE_LT', index=2, number=-1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OBJLANE_OWN', index=3, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OBJLANE_RT', index=4, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OBJLANE_FAR_RT', index=5, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=843,
  serialized_end=990,
)
_sym_db.RegisterEnumDescriptor(_RADAROBJECTDATA_TOBJLANE)

_RADAROBJECTDATA_TOBJCLASS = _descriptor.EnumDescriptor(
  name='TObjClass',
  full_name='pb.ObjectLists.RadarObjectData.TObjClass',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OBJCLASS_UNKONWN', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OBJCLASS_CAR', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OBJCLASS_TRUCK', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OBJCLASS_BIKE', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OBJCLASS_PEDESTRIAN', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OBJCLASS_WIDE_OBJECT', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OBJCLASS_POINT_OBJECT', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OBJCLASS_BRIDGE', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OBJCLASS_GUARDRAIL', index=8, number=8,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=993,
  serialized_end=1206,
)
_sym_db.RegisterEnumDescriptor(_RADAROBJECTDATA_TOBJCLASS)


_RADAROBJECTDATA = _descriptor.Descriptor(
  name='RadarObjectData',
  full_name='pb.ObjectLists.RadarObjectData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='obj_roll_count', full_name='pb.ObjectLists.RadarObjectData.obj_roll_count', index=0,
      number=1, type=17, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_id', full_name='pb.ObjectLists.RadarObjectData.obj_id', index=1,
      number=2, type=17, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_long_displ_m', full_name='pb.ObjectLists.RadarObjectData.obj_long_displ_m', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_vrel_long_ms', full_name='pb.ObjectLists.RadarObjectData.obj_vrel_long_ms', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_accel_long_ms2', full_name='pb.ObjectLists.RadarObjectData.obj_accel_long_ms2', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_prob_of_exist', full_name='pb.ObjectLists.RadarObjectData.obj_prob_of_exist', index=5,
      number=6, type=17, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_dyn_prob', full_name='pb.ObjectLists.RadarObjectData.obj_dyn_prob', index=6,
      number=7, type=17, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_lat_displ_m', full_name='pb.ObjectLists.RadarObjectData.obj_lat_displ_m', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_length', full_name='pb.ObjectLists.RadarObjectData.obj_length', index=8,
      number=9, type=17, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_width', full_name='pb.ObjectLists.RadarObjectData.obj_width', index=9,
      number=10, type=17, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_meas_stat', full_name='pb.ObjectLists.RadarObjectData.obj_meas_stat', index=10,
      number=11, type=17, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_rcs_value_d_bm2', full_name='pb.ObjectLists.RadarObjectData.obj_rcs_value_d_bm2', index=11,
      number=12, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_lat_speed_ms', full_name='pb.ObjectLists.RadarObjectData.obj_lat_speed_ms', index=12,
      number=13, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_obstacle_probability', full_name='pb.ObjectLists.RadarObjectData.obj_obstacle_probability', index=13,
      number=14, type=17, cpp_type=1, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_f_width', full_name='pb.ObjectLists.RadarObjectData.obj_f_width', index=14,
      number=15, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(1.66666663),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_of_interest', full_name='pb.ObjectLists.RadarObjectData.obj_of_interest', index=15,
      number=16, type=13, cpp_type=3, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_lane', full_name='pb.ObjectLists.RadarObjectData.obj_lane', index=16,
      number=17, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=-99,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_class', full_name='pb.ObjectLists.RadarObjectData.obj_class', index=17,
      number=18, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_long_displ_m_std', full_name='pb.ObjectLists.RadarObjectData.obj_long_displ_m_std', index=18,
      number=19, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_lat_displ_m_std', full_name='pb.ObjectLists.RadarObjectData.obj_lat_displ_m_std', index=19,
      number=20, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_vrel_long_ms_std', full_name='pb.ObjectLists.RadarObjectData.obj_vrel_long_ms_std', index=20,
      number=21, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_lat_speed_ms_std', full_name='pb.ObjectLists.RadarObjectData.obj_lat_speed_ms_std', index=21,
      number=22, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='obj_accel_long_ms2_std', full_name='pb.ObjectLists.RadarObjectData.obj_accel_long_ms2_std', index=22,
      number=23, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _RADAROBJECTDATA_TOBJLANE,
    _RADAROBJECTDATA_TOBJCLASS,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=52,
  serialized_end=1206,
)


_RADARSTATUS = _descriptor.Descriptor(
  name='RadarStatus',
  full_name='pb.ObjectLists.RadarStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='radar_CanRXErr', full_name='pb.ObjectLists.RadarStatus.radar_CanRXErr', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='radar_HWFltPrsnt', full_name='pb.ObjectLists.RadarStatus.radar_HWFltPrsnt', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1208,
  serialized_end=1271,
)


_RADAROBJECT = _descriptor.Descriptor(
  name='RadarObject',
  full_name='pb.ObjectLists.RadarObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='header', full_name='pb.ObjectLists.RadarObject.header', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='pb.ObjectLists.RadarObject.data', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='pb.ObjectLists.RadarObject.status', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1274,
  serialized_end=1407,
)

_RADAROBJECTDATA.fields_by_name['obj_lane'].enum_type = _RADAROBJECTDATA_TOBJLANE
_RADAROBJECTDATA.fields_by_name['obj_class'].enum_type = _RADAROBJECTDATA_TOBJCLASS
_RADAROBJECTDATA_TOBJLANE.containing_type = _RADAROBJECTDATA
_RADAROBJECTDATA_TOBJCLASS.containing_type = _RADAROBJECTDATA
_RADAROBJECT.fields_by_name['header'].message_type = header__pb2._HEADER
_RADAROBJECT.fields_by_name['data'].message_type = _RADAROBJECTDATA
_RADAROBJECT.fields_by_name['status'].message_type = _RADARSTATUS
DESCRIPTOR.message_types_by_name['RadarObjectData'] = _RADAROBJECTDATA
DESCRIPTOR.message_types_by_name['RadarStatus'] = _RADARSTATUS
DESCRIPTOR.message_types_by_name['RadarObject'] = _RADAROBJECT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RadarObjectData = _reflection.GeneratedProtocolMessageType('RadarObjectData', (_message.Message,), dict(
  DESCRIPTOR = _RADAROBJECTDATA,
  __module__ = 'RadarObject_pb2'
  # @@protoc_insertion_point(class_scope:pb.ObjectLists.RadarObjectData)
  ))
_sym_db.RegisterMessage(RadarObjectData)

RadarStatus = _reflection.GeneratedProtocolMessageType('RadarStatus', (_message.Message,), dict(
  DESCRIPTOR = _RADARSTATUS,
  __module__ = 'RadarObject_pb2'
  # @@protoc_insertion_point(class_scope:pb.ObjectLists.RadarStatus)
  ))
_sym_db.RegisterMessage(RadarStatus)

RadarObject = _reflection.GeneratedProtocolMessageType('RadarObject', (_message.Message,), dict(
  DESCRIPTOR = _RADAROBJECT,
  __module__ = 'RadarObject_pb2'
  # @@protoc_insertion_point(class_scope:pb.ObjectLists.RadarObject)
  ))
_sym_db.RegisterMessage(RadarObject)


# @@protoc_insertion_point(module_scope)
