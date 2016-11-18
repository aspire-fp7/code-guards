#include "utils.h"

static __inline__ Area* GetNextArea(const Area* current)
{
  return (Area*)((void*)current + sizeof(Area) + sizeof(Block) * current->nr_of_blocks);
}

const Area* GetAreaById(const ADS* ads, uint64_t id)
{
  const Area* area = ads->areas;
  uint32_t iii;
  for(iii = 0; iii < ads->nr_of_areas; iii++)
  {
    if (area->id == id)
      return area;

    area = GetNextArea(area);
  }

  return NULL;
}

void WalkArea(const Area* area, uintptr_t base_address, AttestBlockFun* fun, uint32_t nonce)
{
  uint32_t iii;
  for (iii = 0; iii < area->nr_of_blocks; iii++)
  {
    Block blk = area->blocks[iii];
    fun((uint8_t*)(base_address + (uintptr_t)blk.offset), blk.size);
  }
}
