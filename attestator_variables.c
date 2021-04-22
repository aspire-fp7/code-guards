#include "utils.h"

/* Global variables that will be filled in by Diablo */
#pragma GCC visibility push(hidden)
const ADS data_structure_blob_##LABEL## __attribute__((section (".rodata.data_structure_blob"))) = { 0 };/* Will be resized by Diablo */
const result_t checksum_##LABEL##[1] __attribute__((section (".rodata.checksum"))) = { sizeof(checksum_##LABEL##[0]) };/* Will be resized by Diablo */
#pragma GCC visibility pop
