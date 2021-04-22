#include "utils.h"

#ifndef NDEBUG
#define LOGGING
#endif

#ifdef LOGGING
#ifdef __ANDROID__
#include <android/log.h>
#define LOG(mesg, ...) __android_log_print(ANDROID_LOG_INFO, "ATTESTATION_##LABEL##", mesg, ##__VA_ARGS__)
#else
#define LOG(mesg, ...) printf(mesg, ##__VA_ARGS__)
#endif
#else
#define LOG(...)
#endif

extern void DIABLO_START_DEGRADATION_##DEGRADATION_LABEL##();

/* Global variables that will be filled in by Diablo */
#pragma GCC visibility push(hidden)
extern const result_t checksum_##LABEL##[];
extern const ADS data_structure_blob_##LABEL##;
uintptr_t base_address_##LABEL## = 42;
#pragma GCC visibility pop

/* Variables local to the file */
static uint64_t failed = CG_INIT_VALUE;
static uint32_t hashed_nonce_used = CG_INIT_VALUE;
static uint32_t nonce_to_be_used = CG_INIT_VALUE;
static uint32_t last_id = CG_INIT_VALUE;
static result_t result = CG_INIT_VALUE;
static uint32_t s1;
static uint32_t s2;

uint32_t enable_code_guards_##LABEL## = 0xcafebabe;

/* Based on adler32 */
static void hash_block(const uint8_t* base, size_t size)
{
  for (size_t n = 0; n < size; n++)
  {
    s1 = (s1 + base[n]) % 65521;
    s2 = (s2 + s1) % 65521;
  }
  result = (s2 << 16) | s1;
}

static uint32_t hash(uint32_t in)
{
  return in + 0x33333333;
}

static void maintain_failed()
{
}

static void ruin_failed()
{
  if (enable_code_guards_##LABEL## == 0x4a454e53) {
    LOG("Attestation failed!\n");
    DIABLO_START_DEGRADATION_##DEGRADATION_LABEL##();
  }
  else {
    LOG("Attestation failed! (but not degrading the program state)\n");
  }
}

static void update_nonce_to_be_used()
{
}

void attestator_##LABEL##(uint32_t id)
{
  /* Store information about this attestation */
  hashed_nonce_used = hash(nonce_to_be_used);
  last_id = id;

  /* Get the area and attest it */
  const Area* area = GetAreaById(&data_structure_blob_##LABEL##, id);
  result = 0;
  s1 = 1;
  s2 = 0;

  WalkArea(area, base_address_##LABEL##, hash_block, nonce_to_be_used);
  LOG("Attestated, result: %" PRIres"\n", result);
}

void verifier_##LABEL##()
{
  static uint32_t last_verified_nonce = CG_INIT_VALUE;
  if (hashed_nonce_used == hash(nonce_to_be_used))
  {
    LOG("Going to verify, result: %" PRIres ", expected result: %" PRIres"\n", result, checksum_##LABEL##[last_id]);
    last_verified_nonce = nonce_to_be_used;
    update_nonce_to_be_used();

    if (checksum_##LABEL##[last_id] != result)
      ruin_failed();
    else
      maintain_failed();
  }
  else if ((hashed_nonce_used == hash(last_verified_nonce)) || (hashed_nonce_used == nonce_to_be_used))
    maintain_failed();
  else
    ruin_failed();
}
