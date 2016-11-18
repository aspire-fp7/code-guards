/* C standard headers */
#include <stdint.h>

/* Mechanisms with the number of arguments specified */
#define MECHANISM_NAME(a) DIABLO_REACTION_##a
#define MECHANISM(name, ...) uintptr_t MECHANISM_NAME(name)(uintptr_t first, ##__VA_ARGS__)

/* Degradation function. To work together with the python scripts the name argument to this
 * macro depends on the name of the mechanisms file: mechanisms_${NAME}.c. Example:
 * Filename: mechanisms_easy.c
 * Macro: START_DEGRADATION(easy)
 */
#define START_DEGRADATION_NAME(a) DIABLO_START_DEGRADATION_##a
#define START_DEGRADATION(name, ...) void START_DEGRADATION_NAME(name)(##__VA_ARGS__)

/* Initialization function. To work together with the python scripts the name argument to this
 * macro depends on the name of the mechanisms file: mechanisms_${NAME}.c. Example:
 * Filename: mechanisms_easy.c
 * Macro: INIT_REACTION(easy)
 */
#define INIT_REACTION() static void __attribute__((constructor(65535))) init_reaction()
