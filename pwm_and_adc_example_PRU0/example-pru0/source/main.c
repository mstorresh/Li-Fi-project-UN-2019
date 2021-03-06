#include <stdint.h>
#include <stdio.h>
#include <pru_cfg.h>
#include <rsc_types.h>
#include <limits.h>
#include <sys_pwmss.h>
#include <pru_virtqueue.h>
#include <sys_mailbox.h>
#include <string.h>
#include "resource_table.h"

//Para definir los enteros de 32 bits uint32 //
#include <pru_intc.h>

//Para la comunicacion con ARM //
#include <pru_rpmsg.h>

//Para configurar el PWM//
#include <pru_ecap.h>

//Para las interrupciones Xin/Xout //
#include "pru_common.h"

/* Mapping Constant table reg to variable*/
volatile pruCfg   CT_CFG    __attribute__((cregister("PRU_CFG" , near), peripheral));

#define TO_ARM_HOST       16
#define FROM_ARM_HOST     17

/*
 * Using the name 'rpmsg-pru' will probe the rpmsg_pru driver found
 * at linux-x.y.z/drivers/rpmsg/rpmsg_pru.c
 */
#define CHAN_NAME     "rpmsg-pru"
#define CHAN_DESC     "Channel 30"
#define CHAN_PORT     30

/*
 * Used to make sure the Linux drivers are ready for RPMsg communication
 * Found at linux-x.y.z/include/uapi/linux/virtio_config.h
 */

 //Virtual device is in /dev/rpmsg_pru30

#define VIRTIO_CONFIG_S_DRIVER_OK 4

#define __register__(x) (*((volatile unsigned int *)(x)))

uint8_t payload[RPMSG_BUF_SIZE];//<- definido en pru_rpmsg.h

void configure_adc_module(void);

//Registros para escritura y lectura del PRU //
volatile register uint32_t __R30;
volatile register uint32_t __R31;

//Estructura para compratir datos entre PRU0 y PRU1 //

struct CommSt
{
  char cmd[4]; //Por alineación parece que debe ser de 4
  int32_t d0;
  int32_t d1;
  int32_t d2;
  int32_t d3;
  int32_t d4;
};

// handlers for adc data registers
uint32_t fifo0_count;
uint32_t fifo0_data;

// handlers to store adc read values
uint8_t fifo0_step_id;
uint32_t fifo0_step_value[4];

uint32_t adc_shrd1;
uint32_t adc_shrd2;
uint32_t adc_shrd3;
uint32_t adc_shrd4;

void pwm_config()
{
 
  /* Initialize PRU ECAP for APWM mode */ 
  CT_ECAP.ECCTL2 = 0x02C0; //0000-0010-1100-0000
  
  //Configurar el pwm a 20KHz (1/(5ns cycle * 10000))
  CT_ECAP.CAP1 = 10000; // APRD active register
  CT_ECAP.CAP2 = 0;  //Poner el pwm a 0%
  CT_ECAP.ECCTL2 |= 0x0010;//0000-0000-0001-0000
}

void main(void) {

  struct CommSt* data;
  //Para poder acceder a la información recibida en forma de estructura
  
  volatile uint32_t gpio;
  
  // Inicializar el rpmsg
  //uint32_t prev_gpio_state;
  struct pru_rpmsg_transport transport;
  uint16_t src, dst, len;
  volatile uint8_t *status;
  
  /* Allow OCP master port access by the PRU so the PRU can read external memories */
  CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;
  
  /* Clear the status of the PRU-ICSS system event that the ARM will use to 'kick' us */
  CT_INTC.SICR_bit.STS_CLR_IDX = FROM_ARM_HOST;
  
  /* Make sure the Linux drivers are ready for RPMsg communication */
  status = &resourceTable.rpmsg_vdev.status;
  while (!(*status & VIRTIO_CONFIG_S_DRIVER_OK));
  
  /* Initialize the RPMsg transport structure */
  pru_rpmsg_init(&transport, &resourceTable.rpmsg_vring0, &resourceTable.rpmsg_vring1, TO_ARM_HOST, FROM_ARM_HOST);
  
  /* Create the RPMsg channel between the PRU and ARM user space using the transport structure. */
  while (pru_rpmsg_channel(RPMSG_NS_CREATE, &transport, CHAN_NAME, CHAN_DESC, CHAN_PORT) != PRU_RPMSG_SUCCESS);

  //configIntc();

  pwm_config();

  configure_adc_module();

  while (1)
  {

    // if there is data available in the adc module, gets them

    fifo0_count = __register__(0x44e0d0e4);

    while (fifo0_count > 0) {

      fifo0_data = __register__(0x44e0d100);
      fifo0_step_id = (fifo0_data >> 16) & 0x0f;
      fifo0_step_value[fifo0_step_id] = fifo0_data & 0xfff;
      fifo0_count--;
    }
    
    adc_shrd1 = fifo0_step_value[0];
    adc_shrd2 = fifo0_step_value[1];
    adc_shrd3 = fifo0_step_value[2];
    adc_shrd4 = fifo0_step_value[3];
    CT_INTC.SICR_bit.STS_CLR_IDX = 20;
    __delay_cycles(5);

    /* Check bit 30 of register R31 to see if the ARM has kicked us */
    if (__R31 & HOST0_INT)
    {
      /* Clear the event status */
      CT_INTC.SICR_bit.STS_CLR_IDX = FROM_ARM_HOST;
      /* Receive all available messages, multiple messages can be sent per kick */
      while (pru_rpmsg_receive(&transport, &src, &dst, payload, &len) == PRU_RPMSG_SUCCESS) 
      {

        data = (struct CommSt*) payload;

        /*
        if (len != sizeof(CommSt) || data->cmd[0]!='*')
        {                    
          strncpy(data->cmd ,"#err",4);
          pru_rpmsg_send(&transport, dst, src,payload,len);
          continue;
        }
        */

        //Aunque el protocolo acepta hasta 4 caracteres en la comunicación, por facilidad solo se va
        //a usar un caracter

        switch (data->cmd[1]) {
              
          case 'a': {
          
            // kicks pru1 using host1 interruption
            PRU0_PRU1_TRIGGER;
            data->d1 = adc_shrd1;
            data->d2 = adc_shrd2;
            data->d3 = adc_shrd3;
            data->d4 = adc_shrd4;
            break;
          }
   
          case 'p': {
            
            //Se configura el PWM con un valor entre 0 y 10000 (para encender el LED dim)
            CT_ECAP.CAP3 = data->d0;
            CT_ECAP.CAP4 = data->d1;
            break;
          }        
        }
        pru_rpmsg_send(&transport, dst, src,payload,len);
      }
    }
  }
}

void configure_adc_module(void) {
  // enables the clock
  // (cm_wkup_adc_tsc_clkctrl@cm_wkup)
  __register__(0x44e004bc) = 0x00000002;
  // disables module
  // (ctrl@tsc_adc_ss)
  __register__(0x44e0d040) &= ~0x00000001;
  // sets clock divider
  // (adc_clkdiv@tsc_adc_ss)
  __register__(0x44e0d04c) = 0x00000000;
  // disables all steps
  // (stepenable@tsc_adc_ss)
  __register__(0x44e0d054) = 0x00000000;
  // disables the writing protection for the step configuration registers
  // (ctrl@tsc_adc_ss)
  __register__(0x44e0d040) |= 0x00000004;


  // configures the step 1 to sample using the channel 0, in continuos mode,
  // with an average of 16 samples, enabled by software and to store data in
  // fifo0
  // (stepconfig1@tsc_adc_ss)
  __register__(0x44e0d064) = 0x00000011;
  // sets the open and sample delays of step 1 in 200 cycles
  //0111 0000 0000 0000 0000 1100 1000 = 0xc70000c8
  // (stepdelay1@tsc_adc_ss)
  __register__(0x44e0d068) = 0xc70000c8;


  // configures the step 2 to sample using the channel 1, in continuos mode,
  // with an average of 16 samples, enabled by software and to store data in
  // fifo0
  // (stepconfig2@tsc_adc_ss)
  ///0001 000 0000 0000 0001 0001 = 0x00080011
  __register__(0x44e0d06c) = 0x00080011;
  // sets the open and sample delays of step 2 in 200 cycles
  // (stepdelay2@tsc_adc_ss)
  __register__(0x44e0d070) = 0xc70000c8;


  // configures the step 3 to sample using the channel 2, in continuos mode,
  // with an average of 16 samples, enabled by software and to store data in
  // fifo0
  // (stepconfig3@tsc_adc_ss)
  ///0010 000 0000 0000 0001 0001 = 0x00100011
  __register__(0x44e0d074) = 0x00100011;
  // sets the open and sample delays of step 3 in 200 cycles
  // (stepdelay2@tsc_adc_ss)
  __register__(0x44e0d078) = 0xc70000c8;


  // configures the step 4 to sample using the channel 4, in continuos mode,
  // with an average of 16 samples, enabled by software and to store data in
  // fifo0
  // (stepconfig4@tsc_adc_ss)
  ///0100 000 0000 0000 0001 0001 = 0x00200011
  __register__(0x44e0d07c) = 0x00200011;
  // sets the open and sample delays of step 4 in 200 cycles
  // (stepdelay2@tsc_adc_ss)
  __register__(0x44e0d080) = 0xc70000c8;


  // enables the writing protection for the step configuration registers
  // (register: ctrl@tsc_adc_ss)
  __register__(0x44e0d040) &= ~0x00000004;
  // enables to tag the captured data in the fifo with the step number
  // (ctrl@tsc_adc_ss)
  __register__(0x44e0d040) |= 0x00000002;

  // enables steps 1, 2, 3 and 4
  // (stepenable@tsc_adc_ss)
  __register__(0x44e0d054) = 0x0000001e;

  // enables module
  // (ctrl@tsc_adc_ss)
  __register__(0x44e0d040) |= 0x00000001;
}
