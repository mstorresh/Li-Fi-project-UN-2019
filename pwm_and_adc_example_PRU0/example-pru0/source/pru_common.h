
#ifndef _PRU_COMMON_H_
#define _PRU_COMMON_H_

/* Host-0 Interrupt sets bit 30 in register R31 */
#define HOST0_INT			((uint32_t) 1 << 30)
/* Host-1 Interrupt sets bit 31 in register R31 */
#define HOST1_INT			((uint32_t) 1 << 31)

/* PRU0-to-PRU1 interrupt */
/* Nota, el mapeo de estas interrupciones se hace en resource_table_0.h y
resource_table_1.h*/
#define PRU0_PRU1_EVT   20
#define PRU0_PRU1_TRIGGER	__R31 = ((PRU0_PRU1_EVT - 16) | (1 << 5))

#endif /* _PRU_COMMON_H_ */
