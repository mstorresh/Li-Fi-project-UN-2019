#include <stdint.h>
#include <pru_cfg.h>
#include "resource_table_empty.h"

// El beagle bone puede acceder a algunos pines desde las PRU. Lo que se 
// escribe en el registro __R30, aparece en los pines si estos estan 
// configurados como conectados al pru.
// 
// Como salida se pueden usar los siguientes pines
//
//  Pin   Bit de __R30
//  P8_11 -> 15
//  P8_12 -> 14
//  P9_25 ->  7
//  P9_27 ->  5
//  P9_28 ->  3
//  P9_29 ->  1
//  P9_30 ->  2
//  P9_31 ->  0
//  P9_41 ->  6
//  P9_42 ->  4

volatile register uint32_t __R30;

// Hay algunos pines que se pueden usar como entradas. Estos pines estan mapeados
// al registro __R31, de acuerdo a la siguiente tabla
//
//  Pin   Bit de __R31
//  P8_15 -> 15
//  P8_16 -> 14
//  P9_24 -> 16
//  P9_25 ->  7
//  P9_27 ->  5
//  P9_28 ->  3
//  P9_29 ->  1
//  P9_30 ->  2
//  P9_31 ->  0
//  P9_41 ->  6
//  P9_42 ->  4

volatile register unsigned int __R31;

void main(void)
{
	volatile uint32_t gpio;

	/* Clear SYSCFG[STANDBY_INIT] to enable OCP master port */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

	/* Toggle GPO 7. For PRU 0 this is P9_25 */
	gpio = 1<<7;

	/* Toggle indefinitely at 1 Hz*/
	while (1) {
		__R30 ^= gpio;
		__delay_cycles(100000);
	}
}
