# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: search_files_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1asearch_files_service.proto\x12\x0csearch_files\"4\n\x12SearchFilesRequest\x12\x1e\n\x16\x66ile_to_search_pattern\x18\x01 \x01(\t\"9\n\x13SearchFilesResponse\x12\x13\n\x0bstatus_code\x18\x01 \x01(\x05\x12\r\n\x05\x66iles\x18\x02 \x03(\t2c\n\x0bSearchFiles\x12T\n\rmake_response\x12 .search_files.SearchFilesRequest\x1a!.search_files.SearchFilesResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'search_files_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_SEARCHFILESREQUEST']._serialized_start=44
  _globals['_SEARCHFILESREQUEST']._serialized_end=96
  _globals['_SEARCHFILESRESPONSE']._serialized_start=98
  _globals['_SEARCHFILESRESPONSE']._serialized_end=155
  _globals['_SEARCHFILES']._serialized_start=157
  _globals['_SEARCHFILES']._serialized_end=256
# @@protoc_insertion_point(module_scope)