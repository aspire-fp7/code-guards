/* C standard headers */
#include <stdbool.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>

/* All structs that describe the ADS and its parts. These have to be packed as we'll overlay this structs
 * on directly on ADS we find in the binary.
 */
#pragma pack(1)
typedef struct Block
{
  uint64_t offset;
  uint32_t size;
} Block;

typedef struct Area
{
  uint16_t id;
  uint32_t nr_of_blocks;
  Block blocks[];
} Area;

typedef struct ADS
{
  uint64_t AID_low;
  uint64_t AID_high;
  uint64_t id;
  uint32_t nr_of_areas;
  Area areas[];
} ADS;

/* Typedefs */
typedef void AttestBlockFun(uint8_t* base, size_t size);
typedef uint64_t result_t;
#define PRIres PRIu64

/* General defines */
#define CG_INIT_VALUE 1

/* Functions to be used externally */
const Area* GetAreaById(const ADS* ads, uint64_t id);
void WalkArea(const Area* area, uintptr_t base_address, AttestBlockFun* fun, uint32_t nonce);
