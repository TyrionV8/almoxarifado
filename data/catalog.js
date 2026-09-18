window.CATALOG = {
  "categories": [
    {
      "id": "microcontroladores",
      "name": "Microcontroladores"
    }
  ],
  "column_groups": [
    {
      "id": "acervo",
      "label": "Acervo",
      "position": 1,
      "tone": "green"
    },
    {
      "id": "desempenho",
      "label": "Desempenho e memória",
      "position": 2,
      "tone": "violet"
    },
    {
      "id": "perifericos",
      "label": "Periféricos",
      "position": 3,
      "tone": "blue"
    },
    {
      "id": "eletrica",
      "label": "Elétrica",
      "position": 4,
      "tone": "amber"
    },
    {
      "id": "detalhes",
      "label": "Detalhes",
      "position": 5,
      "tone": "slate"
    }
  ],
  "components": [
    {
      "accelerators": "Nenhum dedicado",
      "adc": "10 bits · 14 canais",
      "category_id": "microcontroladores",
      "clock": 20,
      "cpu": "PIC · 8 bits",
      "dac": "Não",
      "datasheet": "pic16f887.pdf",
      "eeprom": "256 B",
      "estimated": 1,
      "external": "Não",
      "family": "PIC",
      "flash": "8.192 palavras × 14 bits (14 KiB)",
      "flash_short": "14 KiB",
      "gpio": "35 (RE3 somente entrada)",
      "history": [
        {
          "date": "2026-05-07",
          "id": 1,
          "note": "Quantidade estimada no inventário do Obsidian.",
          "quantity": 2,
          "type_id": "entrada"
        }
      ],
      "id": "pic16f887",
      "kind": "chip",
      "logic": "Conforme VDD (2–5,5 V)",
      "mips_peak": 5,
      "name": "PIC16F887-I/P",
      "notes": "RE3/MCLR é somente entrada. Clock máximo depende da tensão. Pinos analógicos precisam de configuração para uso digital.",
      "origin": "Inventario_Componentes_Eletronicos_Obsidian.md · 07/05/2026",
      "oscillator": "Interno até 8 MHz; externo até 20 MHz",
      "package": "PDIP-40",
      "pin_guide": "pic",
      "pinout": "pic16f887.png",
      "pinout_credit": "Microchip Technology · diagrama PDIP-40 e Tabela 3 do datasheet 41291D",
      "pinout_source": "pic16f887.pdf",
      "position": 1,
      "processing_class": "Essencial",
      "programmer": "PICkit 3 · ICSP",
      "pwm": "ECCP + CCP",
      "ram": 368,
      "serial": "EUSART · SPI · I2C (MSSP compartilhado)",
      "stock": {
        "available": 2,
        "in_use": 0,
        "total": 2
      },
      "subtitle": "PDIP-40",
      "temperature": "−40 a +85 °C (sufixo I)",
      "timers": "2 × 8 bits + 1 × 16 bits",
      "use": "Controle geral, muitos sensores, teclado e display paralelo.",
      "voltage": "2–5,5 V"
    },
    {
      "accelerators": "Nenhum dedicado",
      "adc": "10 bits · 4 canais externos",
      "category_id": "microcontroladores",
      "clock": 20,
      "cpu": "PIC · 8 bits",
      "dac": "Não",
      "datasheet": "pic12f675.pdf",
      "eeprom": "128 B",
      "estimated": 1,
      "external": "Não",
      "family": "PIC",
      "flash": "1.024 palavras × 14 bits (1,75 KiB)",
      "flash_short": "1,75 KiB",
      "gpio": "6 (1 somente entrada)",
      "history": [
        {
          "date": "2026-05-07",
          "id": 2,
          "note": "Quantidade estimada no inventário do Obsidian.",
          "quantity": 3,
          "type_id": "entrada"
        }
      ],
      "id": "pic12f675",
      "kind": "chip",
      "logic": "Conforme VDD (2–5,5 V)",
      "mips_peak": 5,
      "name": "PIC12F675-I/P",
      "notes": "Pino 4 (GP3/RA3) somente entrada. Funções compartilham pinos; oscilador externo e MCLR reduzem os sinais livres.",
      "origin": "Inventario_Componentes_Eletronicos_Obsidian.md · 07/05/2026",
      "oscillator": "Interno 4 MHz; externo até 20 MHz",
      "package": "PDIP-8",
      "pin_guide": "pic12",
      "pinout": "pic12f675.png",
      "pinout_credit": "Microchip Technology · diagrama PDIP e Tabela 1-1 do datasheet 41190C",
      "pinout_source": "pic12f675.pdf",
      "position": 2,
      "processing_class": "Essencial",
      "programmer": "PICkit 3 · ICSP",
      "pwm": "Não",
      "ram": 64,
      "serial": "Sem UART, SPI ou I2C por hardware",
      "special": "1 comparador",
      "stock": {
        "available": 3,
        "in_use": 0,
        "total": 3
      },
      "subtitle": "PDIP-8",
      "temperature": "−40 a +85 °C (sufixo I)",
      "timers": "1 × 8 bits + 1 × 16 bits",
      "use": "Botões, temporizadores e sensores simples com pouco espaço.",
      "voltage": "2–5,5 V"
    },
    {
      "accelerators": "Nenhum dedicado",
      "adc": "10 bits · 4 canais externos",
      "category_id": "microcontroladores",
      "clock": 20,
      "cpu": "PIC · 8 bits",
      "dac": "Não",
      "datasheet": "pic12f683.pdf",
      "eeprom": "256 B",
      "estimated": 1,
      "external": "Não",
      "family": "PIC",
      "flash": "2.048 palavras × 14 bits (3,5 KiB)",
      "flash_short": "3,5 KiB",
      "gpio": "6 (1 somente entrada)",
      "history": [
        {
          "date": "2026-05-07",
          "id": 3,
          "note": "Quantidade estimada no inventário do Obsidian.",
          "quantity": 2,
          "type_id": "entrada"
        }
      ],
      "id": "pic12f683",
      "kind": "chip",
      "logic": "Conforme VDD (2–5,5 V)",
      "mips_peak": 5,
      "name": "PIC12F683-I/P",
      "notes": "Pino 4 (GP3/RA3) somente entrada. Funções compartilham pinos; oscilador externo e MCLR reduzem os sinais livres.",
      "origin": "Inventario_Componentes_Eletronicos_Obsidian.md · 07/05/2026",
      "oscillator": "Interno até 8 MHz; externo até 20 MHz",
      "package": "PDIP-8",
      "pin_guide": "pic12",
      "pinout": "pic12f683.png",
      "pinout_credit": "Microchip Technology · diagrama PDIP e Tabela 1 do datasheet 41211D",
      "pinout_source": "pic12f683.pdf",
      "position": 3,
      "processing_class": "Essencial",
      "programmer": "PICkit 3 · ICSP",
      "pwm": "1 CCP · 10 bits",
      "ram": 128,
      "serial": "Sem UART, SPI ou I2C por hardware",
      "special": "1 comparador",
      "stock": {
        "available": 2,
        "in_use": 0,
        "total": 2
      },
      "subtitle": "PDIP-8",
      "temperature": "−40 a +85 °C (sufixo I)",
      "timers": "2 × 8 bits + 1 × 16 bits",
      "use": "Controle compacto de LED, buzzer e sinais PWM.",
      "voltage": "2–5,5 V"
    },
    {
      "accelerators": "CLC · NCO · CWG",
      "adc": "10 bits · 4 canais externos",
      "category_id": "microcontroladores",
      "clock": 20,
      "cpu": "PIC · 8 bits",
      "dac": "5 bits",
      "datasheet": "pic12f1501.pdf",
      "eeprom": "128 B de HEF; sem EEPROM",
      "estimated": 1,
      "external": "Não",
      "family": "PIC",
      "flash": "1.024 palavras × 14 bits (1,75 KiB)",
      "flash_short": "1,75 KiB",
      "gpio": "6 (1 somente entrada)",
      "history": [
        {
          "date": "2026-05-07",
          "id": 4,
          "note": "Quantidade estimada no inventário do Obsidian.",
          "quantity": 3,
          "type_id": "entrada"
        }
      ],
      "id": "pic12f1501",
      "kind": "chip",
      "logic": "Conforme VDD (2–5,5 V)",
      "mips_peak": 5,
      "name": "PIC12F1501-I/P",
      "notes": "Pino 4 (GP3/RA3) somente entrada. Funções compartilham pinos; oscilador externo e MCLR reduzem os sinais livres.",
      "origin": "Inventario_Componentes_Eletronicos_Obsidian.md · 07/05/2026",
      "oscillator": "Interno até 16 MHz; externo até 20 MHz",
      "package": "PDIP-8",
      "pin_guide": "pic12",
      "pinout": "pic12f1501.png",
      "pinout_credit": "Microchip Technology · diagrama e Tabela 1 de alocação do datasheet 40001615C",
      "pinout_source": "pic12f1501.pdf",
      "position": 4,
      "processing_class": "Essencial",
      "programmer": "PICkit 3 · ICSP",
      "pwm": "4 módulos · 10 bits",
      "ram": 64,
      "serial": "Sem UART, SPI ou I2C por hardware",
      "special": "2 CLC · NCO · CWG",
      "stock": {
        "available": 3,
        "in_use": 0,
        "total": 3
      },
      "subtitle": "PDIP-8",
      "temperature": "−40 a +85 °C (sufixo I)",
      "timers": "2 × 8 bits + 1 × 16 bits",
      "use": "Geração de sinais com NCO, CLC e CWG em oito pinos.",
      "voltage": "2,3–5,5 V"
    },
    {
      "accelerators": "Nenhum dedicado",
      "adc": "10 bits · 6 entradas",
      "category_id": "microcontroladores",
      "clock": 16,
      "cpu": "AVR · 8 bits",
      "dac": "Não",
      "datasheet": "atmega328p.pdf",
      "eeprom": "1 KiB",
      "estimated": 0,
      "external": "Não",
      "family": "AVR",
      "flash": "32 KiB (bootloader ocupa parte)",
      "flash_short": "32 KiB",
      "gpio": "20 sinais digitais (inclui A0–A5)",
      "history": [
        {
          "date": "2026-09-12",
          "id": 5,
          "note": "Cadastro inicial do catálogo.",
          "quantity": 1,
          "type_id": "entrada"
        }
      ],
      "id": "uno",
      "kind": "placa",
      "logic": "5 V",
      "mips_peak": 16,
      "name": "Arduino Uno",
      "notes": "Referência Uno R3 com ATmega328P; revisão física não registrada.",
      "origin": "Relato do usuário · 12/09/2026",
      "oscillator": "16 MHz na placa",
      "package": "Placa · ATmega328P",
      "pin_guide": "avr",
      "pinout": "uno-pinout-simple.png",
      "pinout_credit": "Simples: desenho do almoxarifado a partir do datasheet ATmega328P (Figura 1-1, tabela 28.1) e da folha oficial Arduino A000066 · oficial: Arduino, CC BY-SA 4.0",
      "pinout_source": "uno-pinout.pdf",
      "pinouts": [
        {
          "file": "uno-pinout-simple.png",
          "notice": "",
          "title": "Simples · todos os pinos com porta, número no chip e funções"
        },
        {
          "file": "uno-pinout.png",
          "notice": "",
          "title": "Folha oficial Arduino UNO R3 (A000066) · referência"
        }
      ],
      "position": 5,
      "processing_class": "Básico",
      "programmer": "USB com bootloader · ICSP AVR (não PICkit)",
      "pwm": "6 saídas · 8 bits",
      "ram": 2048,
      "serial": "UART · SPI · I2C",
      "stock": {
        "available": 1,
        "in_use": 0,
        "total": 1
      },
      "subtitle": "Placa · ATmega328P",
      "temperature": "Consultar limites da placa e do chip",
      "timers": "2 × 8 bits + 1 × 16 bits",
      "use": "Prototipagem rápida, módulos de 5 V e bibliotecas Arduino.",
      "voltage": "5 V"
    },
    {
      "accelerators": "Nenhum dedicado",
      "adc": "10 bits · 8 entradas",
      "category_id": "microcontroladores",
      "clock": 16,
      "cpu": "AVR · 8 bits",
      "dac": "Não",
      "datasheet": "atmega328p.pdf",
      "eeprom": "1 KiB",
      "estimated": 0,
      "external": "Não",
      "family": "AVR",
      "flash": "32 KiB (bootloader ocupa parte)",
      "flash_short": "32 KiB",
      "gpio": "20 sinais digitais (inclui A0–A5)",
      "history": [
        {
          "date": "2026-09-12",
          "id": 7,
          "note": "Cadastro inicial: um soldado em placa de circuito impresso (PCB) e outro solto.",
          "quantity": 2,
          "type_id": "entrada"
        },
        {
          "date": "2026-09-12",
          "id": 8,
          "note": "Unidade soldada em placa de circuito impresso (PCB).",
          "quantity": 1,
          "type_id": "uso"
        },
        {
          "date": "2026-09-13",
          "id": 14,
          "note": "a que estava soldada, tentei dessoldar e derreti ela :(",
          "quantity": 1,
          "type_id": "descarte_em_uso"
        },
        {
          "date": "2026-09-13",
          "id": 15,
          "note": "Soldado no circuito do Robô equilibrista com o MPU6050",
          "quantity": 1,
          "type_id": "uso"
        }
      ],
      "id": "nano",
      "kind": "placa",
      "logic": "5 V",
      "mips_peak": 16,
      "name": "Arduino Nano",
      "notes": "Um soldado em placa de circuito impresso (PCB), outro solto. Referência Nano clássico ATmega328P; A6/A7 são somente analógicos.",
      "origin": "Relato do usuário · 12/09/2026",
      "oscillator": "16 MHz na placa",
      "package": "Placa · ATmega328P",
      "pin_guide": "avr",
      "pinout": "nano-pinout-simple.png",
      "pinout_credit": "Simples: desenho do almoxarifado a partir do datasheet ATmega328P (Figura 1-1, tabela 28.1) e da folha oficial Arduino A000005 · oficial: Arduino, CC BY-SA 4.0",
      "pinout_source": "nano-pinout.pdf",
      "pinouts": [
        {
          "file": "nano-pinout-simple.png",
          "notice": "",
          "title": "Simples · todos os pinos com porta, número no chip e funções"
        },
        {
          "file": "nano-pinout.png",
          "notice": "",
          "title": "Folha oficial Arduino Nano (A000005) · referência"
        }
      ],
      "position": 6,
      "processing_class": "Básico",
      "programmer": "USB com bootloader · ICSP AVR (não PICkit)",
      "pwm": "6 saídas · 8 bits",
      "ram": 2048,
      "serial": "UART · SPI · I2C",
      "stock": {
        "available": 0,
        "in_use": 1,
        "total": 1
      },
      "subtitle": "Placa · ATmega328P",
      "temperature": "Consultar limites da placa e do chip",
      "timers": "2 × 8 bits + 1 × 16 bits",
      "use": "Prototipagem rápida, módulos de 5 V e bibliotecas Arduino.",
      "voltage": "5 V"
    },
    {
      "accelerators": "Nenhum dedicado",
      "adc": "12 bits · 10 canais externos",
      "category_id": "microcontroladores",
      "clock": 72,
      "coremark": 108.26,
      "coremark_note": "Referência publicada para o STM32F103RB da mesma família; não é uma medição do STM32F103C8 exato.",
      "coremark_per_mhz": 1.5036,
      "cpu": "Cortex-M3 · 32 bits",
      "dac": "Não",
      "datasheet": "stm32f103c8.pdf",
      "dmips": 90,
      "dmips_per_mhz": 1.25,
      "eeprom": "Sem EEPROM",
      "estimated": 0,
      "external": "Não registrada",
      "family": "STM32",
      "flash": "64 KiB",
      "flash_short": "64 KiB",
      "gpio": "Até 37 no chip; depende da placa",
      "history": [
        {
          "date": "2026-09-12",
          "id": 9,
          "note": "Cadastro inicial: duas com USB-C e uma com micro-USB.",
          "quantity": 3,
          "type_id": "entrada"
        }
      ],
      "id": "bluepill",
      "kind": "placa",
      "logic": "3,3 V",
      "name": "BluePill",
      "notes": "STM32F103C8T6 confirmado pelo usuário; duas unidades USB-C e uma micro-USB. Não assumir 128 KiB de Flash: o datasheet C8 declara 64 KiB. USB e CAN compartilham recursos nesta família. Não confundir com o módulo ADS1256 + STM32F103.",
      "origin": "Usuário: três BluePill; associação ao TCC. Marcação STM32F103C8T6 confirmada pelo usuário em 12/09/2026.",
      "oscillator": "8 MHz externo típico; HSI interno 8 MHz",
      "package": "STM32F103C8T6 · LQFP-48",
      "pin_guide": "stm32",
      "pinout": "bluepill-pinout.png",
      "pinout_credit": "Diagrama genérico STM32F103 · Rasmus Friis Kjeldsen (reblag.dk/stm32) · CC BY-SA 4.0",
      "pinout_notice": "Diagrama genérico da placa BluePill STM32F103. As três unidades são STM32F103C8T6, duas com conector USB-C e uma com micro-USB; o desenho mostra a variante micro-USB. Confira a posição do conector e dos jumpers BOOT antes de ligar.",
      "pinout_source": "stm32f103c8.pdf",
      "position": 7,
      "processing_class": "Intermediário",
      "programmer": "ST-Link V2 · SWD; bootloader UART via CH343P",
      "pwm": "Timers com PWM",
      "ram": 20480,
      "relative_bluepill": 1.0,
      "serial": "USART · SPI · I2C · USB FS · CAN 2.0B",
      "stock": {
        "available": 3,
        "in_use": 0,
        "total": 3
      },
      "subtitle": "STM32F103C8T6",
      "temperature": "−40 a +85 °C",
      "timers": "3 gerais + 1 avançado · 16 bits",
      "use": "Controle de sensores, comunicação e temporização com mais memória que os PICs.",
      "variant": "Três unidades STM32F103C8T6: duas com conector USB-C e uma com micro-USB.",
      "voltage": "3,3 V"
    },
    {
      "accelerators": "FPU · DSP",
      "adc": "12 bits · até 10 canais externos",
      "category_id": "microcontroladores",
      "clock": 100,
      "coremark": 339,
      "coremark_per_mhz": 3.39,
      "cpu": "Cortex-M4F · 32 bits · FPU",
      "dac": "Não",
      "datasheet": "stm32f411ce.pdf",
      "dmips": 125,
      "dmips_per_mhz": 1.25,
      "eeprom": "Sem EEPROM",
      "estimated": 0,
      "evidence": "docs/evidence/blackpill-variant.png",
      "external": "8 MiB (8 MB anunciados) · Flash SPI WeAct montada",
      "family": "STM32",
      "flash": "512 KiB",
      "flash_short": "512 KiB",
      "gpio": "Até 36 no chip; pinos ocupados na montagem",
      "history": [
        {
          "date": "2026-09-12",
          "id": 10,
          "note": "Cadastro inicial do catálogo.",
          "quantity": 1,
          "type_id": "entrada"
        },
        {
          "date": "2026-09-12",
          "id": 11,
          "note": "Montagem do TCC.",
          "quantity": 1,
          "type_id": "uso"
        }
      ],
      "id": "blackpill",
      "kind": "placa",
      "logic": "3,3 V",
      "name": "WeAct BlackPill",
      "notes": "No TCC: SPI1 PA4–PA7 para Flash externa; SPI2 PB13–PB15 para ADS1256. O diagrama WeAct v2.0+ é referência, não o mapa de fios da montagem. Não possui DAC nem CAN.",
      "origin": "TCC/DOCUMENTACAO_TECNICA_CRONOLOGICA.md e notas BlackPill do Obsidian; Flash externa de 8 MB confirmada pelo usuário em 12/09/2026",
      "oscillator": "Cristal 25 MHz; núcleo até 100 MHz (96 MHz no TCC)",
      "package": "STM32F411CEU6 · UFQFPN-48",
      "pin_guide": "stm32",
      "pinout": "blackpill-pinout.png",
      "pinout_credit": "WeAct Studio · desenho de Richard Balint",
      "pinout_source": "blackpill-pinout.pdf",
      "position": 8,
      "processing_class": "Avançado",
      "programmer": "ST-Link V2 · SWD; USB DFU; bootloader WeAct usado no TCC",
      "pwm": "Timers com PWM",
      "ram": 131072,
      "relative_bluepill": 1.39,
      "serial": "USART · SPI/I2S · I2C · USB FS · SDIO",
      "stock": {
        "available": 0,
        "in_use": 1,
        "total": 1
      },
      "subtitle": "STM32F411CEU6",
      "temperature": "−40 a +85 °C (chip)",
      "timers": "Até 11 na família, incluindo watchdogs e SysTick",
      "use": "Aquisição e processamento de sinais; já usada com ADS1256 e display no TCC.",
      "variant": "F411 25M HSE 8MFlash",
      "voltage": "3,3 V"
    },
    {
      "accelerators": "FPU · DSP · CORDIC · FMAC",
      "adc": "5 ADCs · 12 bits (canais dependem dos pinos)",
      "category_id": "microcontroladores",
      "clock": 170,
      "coremark": 569,
      "coremark_per_mhz": 3.35,
      "cpu": "Cortex-M4F · 32 bits · FPU · DSP",
      "dac": "7 canais no chip; nem todos externos",
      "datasheet": "stm32g474.pdf",
      "dmips": 213,
      "dmips_per_mhz": 1.25,
      "eeprom": "Sem EEPROM",
      "estimated": 0,
      "external": "Não registrada",
      "family": "STM32",
      "flash": "512 KiB",
      "flash_short": "512 KiB",
      "gpio": "Até 40 no chip; sinais multiplexados",
      "history": [
        {
          "date": "2026-09-12",
          "id": 12,
          "note": "Recém-adquirida; data exata da compra não registrada.",
          "quantity": 1,
          "type_id": "compra"
        }
      ],
      "id": "g474",
      "kind": "placa",
      "logic": "3,3 V",
      "name": "WeAct G474 Long",
      "notes": "128 KiB SRAM = 96 KiB + 32 KiB CCM. Long muda o formato, não a capacidade do chip. Recursos máximos da família não equivalem a canais expostos no encapsulamento de 48 pinos.",
      "origin": "Relato do usuário + conversa “Comparar placas STM32” · CEU6 Long confirmada",
      "oscillator": "HSI interno 16 MHz + PLL; cristal conforme esquema",
      "package": "STM32G474CEU6 · UFQFPN-48",
      "pin_guide": "stm32",
      "pinout": "g474-long-pinout-simple.png",
      "pinout_credit": "Desenhos do almoxarifado · simples: colunas sobre o render oficial WeAct · completa: ST DS12288 Rev 6 (tabelas 12 e 13), esquema WeAct e foto da placa do usuário · pinos numerados pelo UFQFPN48",
      "pinout_source": "g474-long-pinout.pdf",
      "pinouts": [
        {
          "file": "g474-long-pinout-simple.png",
          "notice": "",
          "title": "Simples · GPIO e funções principais"
        },
        {
          "file": "g474-long-pinout-full.png",
          "notice": "",
          "title": "Completa · todas as funções (AF0–AF15 com número + funções adicionais)"
        }
      ],
      "position": 9,
      "processing_class": "Avançado especializado",
      "programmer": "ST-Link V2 · SWD; USB DFU ou UART conforme bootloader",
      "pwm": "HRTIM + timers convencionais",
      "ram": 131072,
      "relative_bluepill": 2.37,
      "schematic": "g474-long-schematic.pdf",
      "serial": "USART/UART · SPI/I2S · I2C · USB FS · FDCAN",
      "special": "CORDIC · FMAC · comparadores · OPAMP · HRTIM",
      "stock": {
        "available": 1,
        "in_use": 0,
        "total": 1
      },
      "subtitle": "STM32G474CEU6",
      "temperature": "−40 a +85 °C (sufixo 6)",
      "timers": "HRTIM de alta resolução + timers avançados e gerais",
      "use": "Controle de potência, conversores, geração de sinais e controle de motores.",
      "voltage": "3,3 V"
    },
    {
      "accelerators": "FPU dupla precisão · DSP · cache · CORDIC",
      "adc": "2 ADCs · 12 bits",
      "category_id": "microcontroladores",
      "clock": 600,
      "coremark": 3196,
      "coremark_per_mhz": 5.33,
      "cpu": "Cortex-M7 · 32 bits · FPU dupla precisão · DSP · cache",
      "dac": "Não",
      "datasheet": "stm32h7r3.pdf",
      "dmips": 1284,
      "dmips_per_mhz": 2.14,
      "eeprom": "Sem EEPROM",
      "estimated": 0,
      "external": "8 MiB Flash na placa (WeAct)",
      "family": "STM32",
      "flash": "64 KiB de boot Flash",
      "flash_short": "64 KiB de boot Flash",
      "gpio": "Conforme conectores no esquema da placa",
      "history": [
        {
          "date": "2026-09-12",
          "id": 13,
          "note": "Recém-adquirida; data exata da compra não registrada.",
          "quantity": 1,
          "type_id": "compra"
        }
      ],
      "id": "h7r3",
      "kind": "placa",
      "logic": "3,3 V",
      "name": "WeAct H7R3",
      "notes": "64 KiB internos são boot Flash; não comparar diretamente com 512 KiB internos da G474. Ethernet exige circuito físico de interface (PHY). Recursos do chip não garantem conectores na placa.",
      "origin": "Modelo informado pelo usuário; documentação oficial WeAct H7R3Zx",
      "oscillator": "Núcleo até 600 MHz via PLL",
      "package": "STM32H7R3Z8J6 · UFBGA-144",
      "pin_guide": "stm32",
      "pinout": "h7-pinout-simple.png",
      "pinout_credit": "Desenhos do almoxarifado a partir do ST DS14360 Rev 3 (tabelas 19 e 20), do esquema e do desenho mecânico WeAct H7R3Zx V1.0 · pinos do CI identificados pela esfera UFBGA144 SMPS GP",
      "pinout_source": "h7-pinout.pdf",
      "pinouts": [
        {
          "file": "h7-pinout-simple.png",
          "notice": "",
          "title": "Visão geral · simples (placa inteira) · clique para ampliar"
        },
        {
          "file": "h7-pinout-full.png",
          "notice": "",
          "title": "Visão geral · completa (placa inteira) · clique para ampliar"
        },
        {
          "file": "h7-pinout-simple-left.png",
          "notice": "",
          "title": "Simples · header esquerdo (P2 + P4)"
        },
        {
          "file": "h7-pinout-simple-right.png",
          "notice": "",
          "title": "Simples · header direito (P1 + P3)"
        },
        {
          "file": "h7-pinout-full-left.png",
          "notice": "",
          "title": "Completa · header esquerdo (P2 + P4) · todas as funções"
        },
        {
          "file": "h7-pinout-full-right.png",
          "notice": "",
          "title": "Completa · header direito (P1 + P3) · todas as funções"
        },
        {
          "file": "h7-pinout-full-extra.png",
          "notice": "",
          "title": "Completa · pinos fora dos headers e notas"
        }
      ],
      "position": 10,
      "processing_class": "Alto desempenho",
      "programmer": "SWD com ferramentas atualizadas para H7RS; verificar suporte do ST-Link V2",
      "pwm": "Timers avançados e gerais",
      "ram": 634880,
      "relative_bluepill": 14.27,
      "schematic": "h7-schematic.pdf",
      "serial": "USART/UART · SPI/I2S · I2C · USB HS/FS · FDCAN · Ethernet",
      "special": "CORDIC · 2 controladores DMA",
      "stock": {
        "available": 1,
        "in_use": 0,
        "total": 1
      },
      "subtitle": "STM32H7R3Z8J6",
      "temperature": "−40 a +85 °C (sufixo 6)",
      "timers": "16 × 16 bits + 4 × 32 bits + 2 watchdogs + SysTick (família)",
      "use": "Processamento intenso e aplicações com código em memória externa.",
      "voltage": "3,3 V"
    },
    {
      "accelerators": "FPU dupla precisão · DSP · cache L1 · Chrom-ART · JPEG",
      "adc": "3 ADCs · 16 bits · até 3,6 MSPS",
      "category_id": "microcontroladores",
      "clock": 480,
      "coremark": 2424,
      "coremark_note": "Valor publicado pela ST para o STM32H743 a 480 MHz (página da série STM32H7); não consta no DS12110 local.",
      "coremark_per_mhz": 5.05,
      "cpu": "Cortex-M7 · 32 bits · FPU dupla precisão · DSP · cache L1 16 + 16 KiB",
      "dac": "2 canais · 12 bits (PA4 e PA5)",
      "datasheet": "stm32h743vi.pdf",
      "dmips": 1027,
      "dmips_per_mhz": 2.14,
      "eeprom": "Sem EEPROM",
      "estimated": 0,
      "external": "8 MB Flash QSPI + 8 MB Flash SPI na placa (WeAct) · microSD",
      "family": "STM32",
      "flash": "2 MiB (2 bancos de 1 MiB)",
      "flash_short": "2 MiB",
      "gpio": "82 no chip (LQFP100); 76 nos headers, vários já ligados a LCD, câmera, microSD e flashes",
      "history": [
        {
          "date": "2026-09-17",
          "id": 16,
          "note": "Recém-adquirida; fotos da placa enviadas pelo usuário. Data exata da compra não registrada.",
          "quantity": 1,
          "type_id": "compra"
        }
      ],
      "id": "h743",
      "kind": "placa",
      "logic": "3,3 V",
      "name": "WeAct H743",
      "notes": "RAM: 1.056 KiB = 864 KiB de SRAM (AXI 512 + SRAM1–3 288 + SRAM4 64) + 192 KiB de TCM (64 ITCM + 128 DTCM), mais 4 KiB de backup; nem todo banco é acessível por todo DMA. A placa ocupa pinos dos headers: TFT em PE10–PE14, câmera DCMI, microSD em PC8–PC12/PD2 e flashes em PB2–PB4/PB6/PD6/PD7/PD11–PD13/PE2. PC2_C/PC3_C são pads analógicos. Ethernet e USB HS precisam de PHY externo.",
      "origin": "Fotos da placa enviadas pelo usuário em 17/09/2026 (chip STM32H743VIT6, serigrafia WeAct Studio); documentação oficial WeActStudio/MiniSTM32H7xx",
      "oscillator": "Cristal 25 MHz (HSE) + 32,768 kHz (LSE); núcleo até 480 MHz via PLL",
      "package": "STM32H743VIT6 · LQFP-100",
      "pin_guide": "stm32",
      "pinout": "h743-pinout-simple.png",
      "pinout_credit": "Desenhos do almoxarifado gerados por scripts/make_h743_pinouts.py a partir do ST DS12110 Rev 7 (tabelas 9–14), do esquema e do desenho mecânico WeAct STM32H7xx V1.2 · pino do CI = número do LQFP100",
      "pinout_source": "h743-pinout.pdf",
      "pinouts": [
        {
          "file": "h743-pinout-simple.png",
          "notice": "",
          "title": "Visão geral · simples (placa inteira) · clique para ampliar"
        },
        {
          "file": "h743-pinout-full.png",
          "notice": "",
          "title": "Visão geral · completa (placa inteira) · clique para ampliar"
        },
        {
          "file": "h743-pinout-simple-left.png",
          "notice": "",
          "title": "Simples · header esquerdo (P2)"
        },
        {
          "file": "h743-pinout-simple-right.png",
          "notice": "",
          "title": "Simples · header direito (P1)"
        },
        {
          "file": "h743-pinout-full-left.png",
          "notice": "",
          "title": "Completa · header esquerdo (P2) · todas as funções"
        },
        {
          "file": "h743-pinout-full-right.png",
          "notice": "",
          "title": "Completa · header direito (P1) · todas as funções"
        },
        {
          "file": "h743-pinout-full-extra.png",
          "notice": "",
          "title": "Completa · pinos fora dos headers e notas"
        }
      ],
      "position": 11,
      "processing_class": "Alto desempenho",
      "programmer": "ST-Link V2 · SWD (conector de 4 furos); USB DFU segurando B0; UART PA9/PA10 pelo bootloader",
      "pwm": "HRTIM + timers avançados e gerais",
      "ram": 1081344,
      "relative_bluepill": 11.41,
      "schematic": "h743-schematic.pdf",
      "serial": "USART/UART · LPUART · SPI/I2S · I2C · USB FS · FDCAN · SDMMC · Ethernet (com PHY)",
      "special": "Câmera DCMI · LCD-TFT · JPEG · Chrom-ART · 2 comparadores · 2 OPAMP · DFSDM",
      "stock": {
        "available": 1,
        "in_use": 0,
        "total": 1
      },
      "subtitle": "STM32H743VIT6",
      "temperature": "−40 a +85 °C (sufixo 6)",
      "timers": "HRTIM + 2 avançados + 10 gerais (2 de 32 bits) + 2 básicos + 5 low-power + 2 watchdogs + SysTick",
      "use": "Câmera e display, processamento de imagem e áudio, DSP em ponto flutuante e registro em microSD.",
      "variant": "WeAct MiniSTM32H7xx · H743VIT6 · TFT 0,96″ · 8 MB QSPI + 8 MB SPI",
      "voltage": "3,3 V"
    }
  ],
  "families": [
    {
      "description": "Microchip PIC de 8 bits",
      "id": "PIC",
      "name": "PIC",
      "position": 1,
      "tone": "orange"
    },
    {
      "description": "Microchip AVR (Arduino)",
      "id": "AVR",
      "name": "AVR",
      "position": 2,
      "tone": "teal"
    },
    {
      "description": "ST Microelectronics Arm Cortex-M",
      "id": "STM32",
      "name": "STM32",
      "position": 3,
      "tone": "blue"
    }
  ],
  "glossary": [
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "Resolução indica quantos códigos existem, não a precisão real. Referência, ruído, impedância da fonte e tempo de aquisição afetam a leitura. Canais multiplexados não significam conversão simultânea.",
      "example": "Um ADC de 12 bits oferece 4096 códigos. O ADS1256 do TCC é externo, não o ADC de 12 bits do F411.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Analog-to-Digital Converter · conversor analógico-digital",
      "position": 1,
      "short": "Transforma uma tensão em um número.",
      "term": "ADC"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "Não são condições normais de operação. Use a faixa operacional recomendada para projetar.",
      "example": "A corrente máxima absoluta de um GPIO não é a corrente recomendada de trabalho.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Limites máximos absolutos",
      "position": 9,
      "short": "Limites além dos quais pode haver dano.",
      "term": "Absolute Maximum Ratings"
    },
    {
      "aliases": [],
      "category_id": "gravacao",
      "detail": "A seleção também pode depender de bits de opção. Consulte o procedimento do modelo antes de entrar no bootloader.",
      "example": "Na BlackPill, BOOT0 e RESET permitem entrar no bootloader de fábrica.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Boot selection pin",
      "position": 5,
      "short": "Sinal que participa da seleção de inicialização.",
      "term": "BOOT0"
    },
    {
      "aliases": [],
      "category_id": "gravacao",
      "detail": "Pode residir em ROM de fábrica ou ocupar parte da Flash do usuário. O endereço de início da aplicação deve corresponder à configuração.",
      "example": "No firmware do TCC com bootloader WeAct, a aplicação começa em 0x08004000.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Carregador de inicialização",
      "position": 4,
      "short": "Programa que inicia ou atualiza a aplicação.",
      "term": "Bootloader"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "O controlador do MCU normalmente precisa de um transceptor externo e terminação adequada. Recursos compartilhados podem limitar operação simultânea.",
      "example": "F103 possui CAN 2.0B; F411 não tem CAN.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Controller Area Network · rede de controladores",
      "position": 10,
      "short": "Barramento robusto para comunicação entre dispositivos.",
      "term": "CAN"
    },
    {
      "aliases": [],
      "category_id": "memoria",
      "detail": "Não assuma que qualquer controlador DMA pode acessar esse banco. Verifique o mapa de barramentos.",
      "example": "32 KiB dos 128 KiB de SRAM do G474 são CCM.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Core-Coupled Memory · memória acoplada ao núcleo",
      "position": 5,
      "short": "Banco de memória com acesso dedicado ao núcleo.",
      "term": "CCM"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "Captura mede o instante de um evento; comparação dispara ao atingir um valor; PWM gera pulsos periódicos.",
      "example": "PIC12F683 tem um CCP; PIC16F887 tem CCP e ECCP.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Capture/Compare/PWM",
      "position": 6,
      "short": "Periférico de captura, comparação e PWM.",
      "term": "CCP"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "Pode implementar funções lógicas sem instruções contínuas da CPU. As fontes e saídas disponíveis são limitadas pelo dispositivo.",
      "example": "PIC12F1501 oferece duas CLC.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Configurable Logic Cell · célula lógica configurável",
      "position": 19,
      "short": "Combina sinais por lógica em hardware.",
      "term": "CLC"
    },
    {
      "aliases": [],
      "category_id": "fundamentos",
      "detail": "Calcula operações como seno e cosseno por um algoritmo iterativo em hardware. Observe formato numérico, escala e precisão configurada.",
      "example": "Disponível no G474 para controle vetorial e cálculo de sinais.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Coordinate Rotation Digital Computer",
      "position": 12,
      "short": "Acelerador de funções trigonométricas.",
      "term": "CORDIC"
    },
    {
      "aliases": [],
      "category_id": "fundamentos",
      "detail": "Clock e arquitetura influenciam desempenho. Frequências iguais não implicam a mesma quantidade de trabalho por segundo.",
      "example": "PIC clássico geralmente executa uma instrução em quatro ciclos de clock; Cortex-M tem outra arquitetura.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Central Processing Unit · unidade central de processamento",
      "position": 2,
      "short": "Núcleo que executa as instruções.",
      "term": "CPU"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Frequentemente ativo em nível baixo. Um periférico pode exigir tempos mínimos entre seleção, clock e desativação.",
      "example": "PA4 é o CS previsto da Flash externa da BlackPill.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Chip Select · seleção do chip",
      "position": 20,
      "short": "Sinal que seleciona o dispositivo SPI.",
      "term": "CS"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "Produz sinais relacionados, com controles como tempo morto, conforme o chip. Não substitui o driver de potência.",
      "example": "PIC12F1501 possui CWG.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Complementary Waveform Generator",
      "position": 18,
      "short": "Gerador de formas de onda complementares.",
      "term": "CWG"
    },
    {
      "aliases": [],
      "category_id": "fundamentos",
      "detail": "O cristal da placa pode ter frequência diferente da CPU: o PLL multiplica ou divide o sinal. Respeite a relação entre tensão e frequência do datasheet.",
      "example": "A BlackPill usa cristal de 25 MHz, admite CPU de 100 MHz e opera em 96 MHz no TCC.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Sinal de sincronização",
      "position": 3,
      "short": "Ritmo de operação do circuito.",
      "term": "Clock"
    },
    {
      "aliases": [],
      "category_id": "fundamentos",
      "detail": "Quanto maior a pontuação, maior o trabalho concluído no teste. Compilador, memória e configuração podem alterar o resultado.",
      "example": "O valor da BluePill é uma referência do STM32F103RB da mesma família, não uma medição do STM32F103C8 exato.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Benchmark CoreMark",
      "position": 8,
      "short": "Teste padronizado de capacidade de processamento de microcontroladores.",
      "term": "CoreMark"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "Confira resolução, faixa de saída, buffer e se o canal chega a um pino externo. PWM filtrado pode aproximar uma saída analógica, mas não é um DAC nativo.",
      "example": "PIC12F1501 tem DAC de 5 bits. F411 não possui DAC.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Digital-to-Analog Converter · conversor digital-analógico",
      "position": 2,
      "short": "Transforma um número em uma tensão analógica.",
      "term": "DAC"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Captura 8 a 14 bits por pulso de PIXCLK, sincronizados por HSYNC e VSYNC, normalmente com DMA para a RAM. O sensor é configurado à parte por I2C (SCCB).",
      "example": "H743 WeAct: conector de câmera de 24 vias para OV2640, OV7725 ou OV5640.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Digital Camera Interface · interface de câmera digital",
      "position": 25,
      "short": "Recebe imagem de sensores com barramento paralelo (DVP).",
      "term": "DCMI"
    },
    {
      "aliases": [],
      "category_id": "gravacao",
      "detail": "Depende de bootloader e do modo de inicialização. Uma porta USB presente na placa não garante DFU em qualquer configuração.",
      "example": "A BlackPill F411 pode usar o bootloader de fábrica por USB.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Device Firmware Upgrade · atualização de firmware",
      "position": 3,
      "short": "Protocolo USB para carregar firmware.",
      "term": "DFU"
    },
    {
      "aliases": [],
      "category_id": "fundamentos",
      "detail": "Um controlador move dados entre periféricos e memória. Confira bancos acessíveis, largura das transferências e coerência de cache.",
      "example": "É útil para receber amostras SPI em buffers.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Direct Memory Access · acesso direto à memória",
      "position": 11,
      "short": "Transfere dados sem a CPU copiar cada item.",
      "term": "DMA"
    },
    {
      "aliases": [],
      "category_id": "fundamentos",
      "detail": "É uma medição diferente de MIPS. Aqui permite comparar os STM32 usando números publicados pela STMicroelectronics.",
      "example": "A BluePill tem 90 DMIPS; ela é a referência 1,00× da coluna de desempenho relativo.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Dhrystone Million Instructions Per Second",
      "position": 7,
      "short": "Resultado normalizado do teste Dhrystone.",
      "term": "DMIPS"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "Relaciona-se a códigos ausentes e monotonicidade. Resolução nominal não descreve essa variação.",
      "example": "Confira a tabela ADC do componente quando a precisão importa.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Differential Nonlinearity · não linearidade diferencial",
      "position": 12,
      "short": "Variação do tamanho de cada passo de conversão.",
      "term": "DNL"
    },
    {
      "aliases": [],
      "category_id": "fundamentos",
      "detail": "Instruções DSP aceleram tarefas como multiplicar e acumular. Não substituem planejamento da amostragem, memória e fluxo de dados.",
      "example": "Filtros de sinais adquiridos pelo TCC podem aproveitar instruções do Cortex-M4.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Digital Signal Processing · processamento digital de sinais",
      "position": 10,
      "short": "Operações para filtrar e analisar sinais.",
      "term": "DSP"
    },
    {
      "aliases": [],
      "category_id": "fisico",
      "detail": "Reúne pinagem, limites elétricos e temporizações. O manual de referência explica registros; errata registra limitações conhecidas.",
      "example": "Use o datasheet local para limites completos; a tabela do acervo resume critérios de escolha.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Folha de dados do fabricante",
      "position": 3,
      "short": "Documento de especificações do componente.",
      "term": "Datasheet"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "Pode oferecer saídas e modos para acionamento de pontes conforme o modelo. Configuração e pinos limitam o uso.",
      "example": "PIC16F887 inclui ECCP.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Enhanced Capture/Compare/PWM",
      "position": 7,
      "short": "Versão ampliada do periférico CCP.",
      "term": "ECCP"
    },
    {
      "aliases": [],
      "category_id": "memoria",
      "detail": "Permite gravar configurações e contadores; observe resistência de escrita e tempo de gravação. Emular EEPROM em Flash exige gerenciar apagamento e desgaste.",
      "example": "PIC16F887 tem 256 bytes; PIC12F1501 oferece HEF no lugar da EEPROM clássica.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Electrically Erasable Programmable Read-Only Memory",
      "position": 3,
      "short": "Memória não volátil para pequenos dados.",
      "term": "EEPROM"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "É obtido sob condições de ensaio, frequentemente por relação sinal-ruído e distorção. Não equivale simplesmente ao número de bits do registrador.",
      "example": "Um ADC nominal de 12 bits pode ter ENOB menor.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Effective Number of Bits · número efetivo de bits",
      "position": 13,
      "short": "Resolução efetiva considerando ruído e distorção.",
      "term": "ENOB"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Acrescenta recursos conforme o modelo, como detecção de baud rate. Consulte o capítulo do periférico.",
      "example": "PIC16F887 possui EUSART para comunicação serial.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Enhanced USART",
      "position": 5,
      "short": "Interface serial universal aprimorada.",
      "term": "EUSART"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Permite maior carga útil e taxa na fase de dados. Não dispensa transceptor compatível. Quantidade e pinos variam por modelo.",
      "example": "G474 e H7R3 têm FDCAN; a placa não necessariamente inclui transceptor.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Flexible Data-rate CAN · CAN com taxa de dados flexível",
      "position": 11,
      "short": "Controlador CAN com suporte a quadros CAN FD.",
      "term": "FDCAN"
    },
    {
      "aliases": [],
      "category_id": "fundamentos",
      "detail": "Ajuda a executar filtros digitais. Coeficientes, escalonamento e saturação precisam ser configurados.",
      "example": "G474 possui FMAC; F411 utiliza CPU e instruções DSP.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Filter Math Accelerator · acelerador matemático de filtros",
      "position": 13,
      "short": "Hardware dedicado a cálculos de filtragem.",
      "term": "FMAC"
    },
    {
      "aliases": [],
      "category_id": "fundamentos",
      "detail": "A precisão suportada depende do núcleo. O compilador precisa configurar corretamente a geração das instruções.",
      "example": "F411 e G474 possuem FPU de precisão simples; BluePill Cortex-M3 não.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Floating-Point Unit · unidade de ponto flutuante",
      "position": 9,
      "short": "Hardware que acelera contas com números fracionários.",
      "term": "FPU"
    },
    {
      "aliases": [],
      "category_id": "memoria",
      "detail": "É apagada em blocos e tem limite de ciclos de escrita. Flash externa não é automaticamente equivalente à memória interna para executar código.",
      "example": "H7R3: 64 KiB internos para boot e 8 MiB externos na placa WeAct.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Memória não volátil regravável",
      "position": 1,
      "short": "Guarda o programa mesmo sem energia.",
      "term": "Flash"
    },
    {
      "aliases": [],
      "category_id": "gravacao",
      "detail": "Controlam clock, reset, proteção e outros comportamentos. Em STM32 funções parecidas usam option bytes.",
      "example": "Uma configuração de clock incorreta pode impedir a execução esperada no PIC.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Bits de configuração",
      "position": 8,
      "short": "Configurações persistentes do microcontrolador.",
      "term": "Fuses"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "Dispositivos ligados por sinais elétricos precisam compartilhar uma referência adequada. Terra de circuito não implica terra de proteção.",
      "example": "Una GND do adaptador serial ao GND da placa.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Ground · terra de referência",
      "position": 3,
      "short": "Referência comum de tensão do circuito.",
      "term": "GND"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Pinos podem compartilhar funções e nem todos aceitam saída. Contagem do chip, pinos expostos na placa e pinos livres no projeto são coisas diferentes.",
      "example": "Nos PICs de oito pinos, GP3/RA3 é somente entrada.",
      "figure": null,
      "figure_caption": null,
      "meaning": "General-Purpose Input/Output · entrada/saída de uso geral",
      "position": 1,
      "short": "Pino configurável para ler ou produzir sinais digitais.",
      "term": "GPIO"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Tolerância não se aplica automaticamente em modo analógico nem com o chip desligado. Não significa que o pino produz 5 V na saída.",
      "example": "Consulte a coluna de tipo de I/O no datasheet STM32 antes de conectar módulos de 5 V.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Entrada tolerante a 5 V",
      "position": 2,
      "short": "Alguns pinos aceitam 5 V sob condições específicas.",
      "term": "GPIO 5 V tolerant"
    },
    {
      "aliases": [],
      "category_id": "memoria",
      "detail": "Não é EEPROM convencional; respeite sequência de apagamento e escrita e os limites do fabricante.",
      "example": "PIC12F1501 oferece 128 bytes de HEF.",
      "figure": null,
      "figure_caption": null,
      "meaning": "High-Endurance Flash · Flash de alta resistência",
      "position": 4,
      "short": "Área Flash destinada a dados gravados com frequência.",
      "term": "HEF"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "Útil em conversores de potência com saídas complementares, sincronização e proteção. A resolução fina não equivale ao período mínimo completo.",
      "example": "É um diferencial do G474 para controle de potência.",
      "figure": null,
      "figure_caption": null,
      "meaning": "High-Resolution Timer · temporizador de alta resolução",
      "position": 5,
      "short": "Temporizador para controle preciso de pulsos.",
      "term": "HRTIM"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "Pode usar cristal ou sinal externo conforme configuração. Capacitores e modo de oscilador precisam corresponder ao circuito.",
      "example": "BlackPill: cristal HSE de 25 MHz.",
      "figure": null,
      "figure_caption": null,
      "meaning": "High-Speed External oscillator",
      "position": 14,
      "short": "Fonte externa de clock de alta frequência.",
      "term": "HSE"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "Dispensa cristal externo, mas precisão varia conforme o dispositivo e condições. Calibração pode ser relevante.",
      "example": "STM32G474 inclui HSI de 16 MHz.",
      "figure": null,
      "figure_caption": null,
      "meaning": "High-Speed Internal oscillator",
      "position": 15,
      "short": "Oscilador interno de alta frequência.",
      "term": "HSI"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Usa endereços e saídas de dreno aberto com resistores pull-up. Verifique tensão dos pull-ups, capacitância e endereços repetidos.",
      "example": "Sensores e displays podem compartilhar o barramento, desde que os endereços sejam compatíveis.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Inter-Integrated Circuit · barramento entre circuitos",
      "position": 8,
      "short": "Comunicação por duas linhas: SDA e SCL.",
      "term": "I2C"
    },
    {
      "aliases": [],
      "category_id": "gravacao",
      "detail": "No PIC usa MCLR/VPP, VDD, VSS, dados e clock. O conector AVR também chamado ICSP tem sinais e protocolo diferentes.",
      "example": "PICkit 3 para PICs; não tratar ICSP do Arduino como compatível com PICkit.",
      "figure": null,
      "figure_caption": null,
      "meaning": "In-Circuit Serial Programming · programação no circuito",
      "position": 2,
      "short": "Gravação sem remover o microcontrolador da montagem.",
      "term": "ICSP"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "O consumo varia com clock, temperatura, tensão e periféricos ativos. Valores típicos não são garantias de máximo.",
      "example": "Compare chips sob condições equivalentes para projetos a bateria.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Supply Current",
      "position": 8,
      "short": "Corrente consumida pela alimentação do circuito.",
      "term": "IDD"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "Geralmente expresso em LSB; afeta a exatidão ao longo da faixa. Consulte o método usado pelo fabricante.",
      "example": "É uma especificação importante para comparar ADCs além da resolução.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Integral Nonlinearity · não linearidade integral",
      "position": 11,
      "short": "Desvio da transferência real em relação à reta ideal.",
      "term": "INL"
    },
    {
      "aliases": [],
      "category_id": "fundamentos",
      "detail": "Prioridade e tempo de atendimento afetam a resposta. Evite operações demoradas nas rotinas críticas.",
      "example": "Um sinal de amostra pronta pode disparar uma interrupção.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Interrupção",
      "position": 15,
      "short": "Evento que desvia a execução para uma rotina de atendimento.",
      "term": "Interrupt"
    },
    {
      "aliases": [],
      "category_id": "fisico",
      "detail": "Um KiB contém 1024 bytes; um MiB contém 1048576 bytes. Fabricantes frequentemente escrevem KB para capacidades binárias.",
      "example": "512 KiB = 524288 bytes. Palavras de 14 bits dos PICs precisam ser descritas separadamente.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Kibibyte · 1024 bytes",
      "position": 1,
      "short": "Unidade binária de capacidade de memória.",
      "term": "KiB"
    },
    {
      "aliases": [
        "LPUART1"
      ],
      "category_id": "comunicacao",
      "detail": "É uma UART (TX, RX e, se quiser, RTS/CTS e DE) feita para gastar pouco: ela continua recebendo com o chip em modo Stop e acorda a CPU quando chega algo. Os quadros são iguais aos de qualquer UART (start, dados, paridade, stop), então do outro lado pode estar qualquer UART comum.\n\nO segredo é o clock. O LPUART pode usar o cristal LSE de 32,768 kHz, que continua ligado no Stop. O baud rate vem de um divisor fracionário, BRR = 256 × f_clock ÷ baud: com o LSE, 9600 bit/s dá BRR ≈ 874 e erro de só 0,02 %. Como o BRR mínimo é 0x300, o limite é f_clock ÷ 3; na prática, 9600 bit/s com o LSE. Para 115 200 bit/s ou mais, use HSI, CSI ou o clock do barramento, e o consumo sobe.\n\nO despertar pode ser programado para o start bit, para qualquer quadro, para um byte específico (endereço) ou para o estado da FIFO. No STM32H743 o LPUART1 fica no domínio D3, junto com o RCC, a SRAM4 e o BDMA. Esse domínio pode seguir funcionando com D1 (CPU) e D2 (onde ficam os USART) desligados. O DMA que atende o LPUART1 é o BDMA, que trabalha com a SRAM4: confira no manual de referência RM0433 antes de montar o buffer.\n\nEm troca, perde recursos: não tem modo síncrono, LIN, IrDA, Smartcard, detecção automática de baud rate nem timeout de recepção. Use o LPUART para sensores, GPS, modems ou outro microcontrolador que enviam dados de vez em quando enquanto o sistema dorme; para console e gravação, um USART comum é mais simples.",
      "example": "H743 WeAct: LPUART1 em PA9 (TX) e PA10 (RX), função alternativa AF3 — os mesmos pinos do USART1 (AF7), então só um dos dois usa o par. O cristal LSE de 32,768 kHz já está montado na placa (PC14/PC15). A G474 também tem LPUART1; F411 e F103 não têm.",
      "figure": "assets/glossary/lpuart.svg",
      "figure_caption": "O que continua ligado no modo Stop (LSE e LPUART1 no domínio D3), o consumo ao longo do tempo com o despertar por um quadro recebido, o cálculo do baud rate com 32,768 kHz e a comparação com os USART do H743.",
      "meaning": "Low-Power Universal Asynchronous Receiver/Transmitter · UART de baixo consumo",
      "position": 6,
      "short": "UART que continua recebendo com o chip em modo Stop, usando o cristal de 32,768 kHz, e acorda a CPU só quando chega um dado.",
      "term": "LPUART"
    },
    {
      "aliases": [],
      "category_id": "fisico",
      "detail": "O número de pinos é do chip, não de sinais digitais livres. Alimentação e funções reservadas ocupam terminais.",
      "example": "STM32F103C8T6 usa LQFP de 48 pinos.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Low-profile Quad Flat Package",
      "position": 5,
      "short": "Encapsulamento fino com terminais em quatro lados.",
      "term": "LQFP"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "No ADC ideal, o passo é aproximadamente a faixa de referência dividida pelo número de códigos. Precisão real inclui outros erros.",
      "example": "12 bits oferecem 4096 códigos, mas não garantem 12 bits livres de ruído.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Least Significant Bit · bit menos significativo",
      "position": 10,
      "short": "Menor passo do código digital.",
      "term": "LSB"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "Normalmente um cristal de 32,768 kHz para relógio de tempo real. Confira se a placa tem o cristal instalado.",
      "example": "A existência do periférico RTC não confirma cristal LSE na placa.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Low-Speed External oscillator",
      "position": 16,
      "short": "Fonte externa de baixa frequência.",
      "term": "LSE"
    },
    {
      "aliases": [],
      "category_id": "gravacao",
      "detail": "Pode compartilhar a função VPP de programação. Dependendo dos bits de configuração pode virar entrada digital, nunca assuma uma saída.",
      "example": "Pino 4 dos PICs de oito pinos compartilha MCLR e VPP.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Master Clear · reinicialização principal",
      "position": 7,
      "short": "Entrada de reset dos PICs.",
      "term": "MCLR"
    },
    {
      "aliases": [],
      "category_id": "fundamentos",
      "detail": "Executa o firmware e controla entradas e saídas. Uma placa adiciona alimentação, conectores e outros circuitos ao MCU.",
      "example": "A BlackPill é a placa; STM32F411CEU6 é o MCU.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Microcontroller Unit · unidade microcontroladora",
      "position": 1,
      "short": "Chip que reúne processador, memória e periféricos.",
      "term": "MCU"
    },
    {
      "aliases": [],
      "category_id": "fundamentos",
      "detail": "É unidade de frequência, não de instruções executadas por segundo. Considere arquitetura, memória e periféricos.",
      "example": "100 MHz é o limite da CPU do F411; o cristal de 25 MHz é outra referência.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Megahertz",
      "position": 4,
      "short": "Um milhão de ciclos por segundo.",
      "term": "MHz"
    },
    {
      "aliases": [],
      "category_id": "fundamentos",
      "detail": "Neste catálogo, é usado para PIC e ATmega328P. Não deve ser comparado diretamente com DMIPS ou CoreMark.",
      "example": "Os PIC de 20 MHz chegam a 5 MIPS; o ATmega328P de 16 MHz chega a 16 MIPS.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Milhões de instruções por segundo",
      "position": 6,
      "short": "Indica o pico de instruções executadas por segundo.",
      "term": "MIPS"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Também chamada CIPO, Controller In Peripheral Out. Dispositivos não selecionados devem liberar a linha quando compartilhada.",
      "example": "PB14 recebe dados do ADS1256 via SPI2 no TCC.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Master In Slave Out",
      "position": 14,
      "short": "Linha SPI do periférico para o controlador.",
      "term": "MISO"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Também chamada COPI, Controller Out Peripheral In. Conecte os sinais conforme a direção definida no dispositivo.",
      "example": "PB15 é usado como saída SPI2 para ADS1256 no TCC.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Master Out Slave In",
      "position": 13,
      "short": "Linha SPI do controlador para o periférico.",
      "term": "MOSI"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "É taxa de conversão, não frequência de CPU. Banda útil e precisão dependem da configuração.",
      "example": "ADCs rápidos do G474 são úteis para controle, desde que a entrada estabilize.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Million Samples Per Second",
      "position": 16,
      "short": "Milhões de amostras por segundo.",
      "term": "MSPS"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Pode operar como SPI ou I2C. Um único módulo não executa as duas interfaces ao mesmo tempo.",
      "example": "PIC16F887 oferece SPI e I2C pelo MSSP compartilhado.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Master Synchronous Serial Port",
      "position": 12,
      "short": "Periférico de comunicação síncrona dos PICs.",
      "term": "MSSP"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "Não confunda limite operacional garantido com limite absoluto de dano.",
      "example": "Clock máximo depende da alimentação em vários PICs.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Maximum · máximo",
      "position": 12,
      "short": "Maior valor especificado nas condições da tabela.",
      "term": "Max"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "Leia unidades e condições: um mínimo pode indicar um requisito que seu circuito precisa atender.",
      "example": "VIH mínimo define a tensão necessária para entrada alta.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Minimum · mínimo",
      "position": 11,
      "short": "Menor valor especificado nas condições da tabela.",
      "term": "Min"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "Um acumulador recebe incrementos a cada clock. O valor do incremento determina a frequência média de saída.",
      "example": "PIC12F1501 inclui NCO para geração de sinais.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Numerically Controlled Oscillator · oscilador controlado numericamente",
      "position": 17,
      "short": "Gera pulsos por acumulação numérica.",
      "term": "NCO"
    },
    {
      "aliases": [],
      "category_id": "gravacao",
      "detail": "O prefixo N indica ativação em nível baixo. Reset não é desligamento e não apaga a Flash.",
      "example": "ST-Link pode usar NRST para conectar sob reset.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Reset ativo em nível baixo",
      "position": 6,
      "short": "Pino que reinicia o microcontrolador.",
      "term": "NRST"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "Modelos integrados podem conectar sinais internamente. Faixa de entrada, ganho, banda e pinos expostos limitam o uso.",
      "example": "G474 inclui amplificadores operacionais para aplicações analógicas.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Operational Amplifier · amplificador operacional",
      "position": 8,
      "short": "Amplifica a diferença entre duas entradas.",
      "term": "OPAMP"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Precisa de pull-up para obter nível alto. Permite vários participantes compartilharem o sinal.",
      "example": "I2C utiliza essa forma de saída.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Saída de dreno aberto",
      "position": 22,
      "short": "Saída que puxa para baixo ou fica em alta impedância.",
      "term": "Open Drain"
    },
    {
      "aliases": [],
      "category_id": "fisico",
      "detail": "O layout físico define quais sinais estão conectados e quais chegam aos conectores.",
      "example": "Um dos seus Nano está soldado em uma PCB.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Printed Circuit Board · placa de circuito impresso",
      "position": 8,
      "short": "Placa que interliga eletricamente os componentes.",
      "term": "PCB"
    },
    {
      "aliases": [],
      "category_id": "fisico",
      "detail": "O número indica quantidade total de pinos. Identifique entalhe e pino 1 antes de ligar.",
      "example": "PIC16F887-I/P tem PDIP de 40 pinos.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Plastic Dual In-line Package",
      "position": 4,
      "short": "Encapsulamento plástico com duas fileiras de terminais.",
      "term": "PDIP"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Ter um controlador Ethernet no chip não significa ter o PHY, conector e demais componentes na placa.",
      "example": "Consulte o esquema antes de planejar Ethernet com H7R3.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Physical Layer · camada física",
      "position": 23,
      "short": "Circuito que traduz sinais digitais para o meio físico.",
      "term": "PHY"
    },
    {
      "aliases": [],
      "category_id": "fundamentos",
      "detail": "Multiplicadores e divisores devem respeitar as faixas internas. Periféricos como USB exigem clocks específicos.",
      "example": "O TCC configura CPU do F411 em 96 MHz e USB em 48 MHz.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Phase-Locked Loop · malha de captura de fase",
      "position": 5,
      "short": "Circuito que gera clocks derivados de uma referência.",
      "term": "PLL"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "Duty cycle é o tempo ligado dividido pelo período. Frequência e resolução dependem do clock e do timer. Para motores ou cargas, use estágio de potência adequado.",
      "example": "PIC12F675 não tem PWM por hardware; PIC12F683 tem um CCP.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Pulse-Width Modulation · modulação por largura de pulso",
      "position": 3,
      "short": "Controla a proporção de tempo em nível alto.",
      "term": "PWM"
    },
    {
      "aliases": [],
      "category_id": "fisico",
      "detail": "Confira vista superior ou inferior, referência do pino 1, encapsulamento e revisão da placa. Funções alternativas no mesmo pino não operam todas simultaneamente.",
      "example": "O mapa da G474 Long é diferente do layout compacto mesmo com o mesmo MCU.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Mapa de pinagem",
      "position": 2,
      "short": "Desenho que relaciona pinos e funções.",
      "term": "Pinout"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Evita entrada flutuante e permite barramentos de dreno aberto. O valor depende de corrente e velocidade desejadas.",
      "example": "SDA e SCL em I2C precisam de pull-ups apropriados.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Resistor para a alimentação positiva",
      "position": 21,
      "short": "Mantém uma linha em nível alto quando ninguém a aciona.",
      "term": "Pull-up"
    },
    {
      "aliases": [
        "Quad-SPI",
        "QUADSPI",
        "Quad SPI"
      ],
      "category_id": "memoria",
      "detail": "Ligação: CLK e NCS (seleção, ativa em nível baixo) mais IO0–IO3. As quatro linhas são bidirecionais: IO0 e IO1 fazem o papel de MOSI e MISO quando a memória fala SPI comum, e IO2/IO3 são os antigos /WP e /HOLD da Flash. Por isso a mesma Flash funciona em SPI (1 linha), Dual (2) ou Quad (4); o modo quad normalmente precisa ser liberado pelo bit QE do registrador de status da memória.\n\nCada acesso tem fases: instrução (8 bits, muitas vezes numa linha só), endereço (24 bits até 16 MB; 32 bits acima), bytes de modo, ciclos dummy (tempo para a memória buscar o dado) e dados. No comando EBh, notação 1-4-4, a instrução usa 1 linha e endereço e dados usam 4: cada byte passa em 2 clocks, contra 8 no SPI comum. Comando, largura de cada fase e número de dummy precisam bater com o datasheet da Flash; um valor errado desloca todos os bits lidos.\n\nO periférico QUADSPI do STM32H743 tem três modos: indireto (o programa envia comandos e lê ou grava por registrador ou DMA), polling de status (espera a Flash terminar uma gravação sem ocupar a CPU) e mapeado em memória (a Flash aparece a partir de 0x9000 0000 e pode ser lida, e até executada, como memória comum, passando pelo cache). Gravar e apagar exige o modo indireto: apague setores de 4 KiB antes e grave em páginas de até 256 bytes.\n\nVelocidade: a QUADSPI do H743 chega a 133 MHz (DS12110), mas o limite real depende da Flash, do comando e das trilhas; comece com o divisor de clock alto e suba. Diferente do SPI, não é um barramento para vários periféricos: cada banco atende uma memória (os dois bancos juntos formam o modo Dual-Flash de 8 bits).",
      "example": "H743 WeAct: Flash PY25Q64HA de 8 MB no QUADSPI banco 1 — CLK PB2, NCS PB6, IO0 PD11, IO1 PD12, IO2 PE2 e IO3 PD13 (esses pinos também saem nos headers). Mapeada em 0x9000 0000, guarda imagens e fontes do display ou código. A H7R3 usa o XSPI no mesmo papel.",
      "figure": "assets/glossary/qspi.svg",
      "figure_caption": "Em cima, a diferença de ligação entre SPI e QSPI, com os pinos da Flash QSPI da H743. Embaixo, uma leitura EBh clock a clock: instrução em uma linha, endereço, modo, dummy e dados em quatro linhas.",
      "meaning": "Quad Serial Peripheral Interface · SPI de quatro linhas de dados (Quad-SPI, QUADSPI)",
      "position": 7,
      "short": "Versão do SPI que usa quatro linhas de dados ao mesmo tempo para ler e gravar memória Flash externa até 4× mais rápido. No STM32 ela também deixa o programa ler, e até executar código, direto da Flash externa.",
      "term": "QSPI"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "Pode permanecer ativo com alimentação de backup. Precisão depende da fonte de clock e calibração.",
      "example": "VBAT pode alimentar o domínio de backup de STM32.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Real-Time Clock · relógio de tempo real",
      "position": 17,
      "short": "Periférico que mantém a contagem de tempo.",
      "term": "RTC"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Recebe o TX do outro dispositivo. Compatibilidade de tensão e referência de terra são necessárias.",
      "example": "RX do CH343P recebe o TX da placa.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Receive · recepção",
      "position": 19,
      "short": "Sinal de entrada de dados seriais.",
      "term": "RX"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Em SPI, frequência, polaridade e fase precisam corresponder às exigências do periférico.",
      "example": "PB13 fornece SCK do SPI2 na montagem do TCC.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Serial Clock",
      "position": 15,
      "short": "Clock que sincroniza os bits da interface serial.",
      "term": "SCK"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Normalmente usa pull-up. Resistência e capacitância afetam o tempo de subida e a velocidade possível.",
      "example": "No Uno, A5 corresponde a SCL.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Serial Clock Line",
      "position": 17,
      "short": "Linha de clock do barramento I2C.",
      "term": "SCL"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "É bidirecional e normalmente precisa de pull-up. A tensão do pull-up define o nível alto.",
      "example": "No Uno, A4 corresponde a SDA.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Serial Data",
      "position": 16,
      "short": "Linha de dados do barramento I2C.",
      "term": "SDA"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Usa CLK, CMD e D0–D3; costuma ser acompanhado de biblioteca de sistema de arquivos (FAT). Pull-ups e comprimento das trilhas afetam a velocidade máxima.",
      "example": "H743 WeAct: microSD no SDMMC1 (PC8–PC12 e PD2), detecção em PD4.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Secure Digital / MultiMediaCard interface",
      "position": 24,
      "short": "Controlador de cartão SD em barramento de 1 ou 4 bits.",
      "term": "SDMMC"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "É frequentemente expressa em decibéis. Banda, amplitude e configuração de teste precisam acompanhar o número.",
      "example": "Útil na análise da cadeia de aquisição do TCC.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Signal-to-Noise Ratio · relação sinal-ruído",
      "position": 14,
      "short": "Relação entre potência do sinal e do ruído.",
      "term": "SNR"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Sinais: SCK é o clock, sempre gerado pelo controlador; MOSI leva dados do controlador ao periférico e MISO traz de volta (nomes novos: COPI/CIPO, ou SDO/SDI vistos de cada chip); CS, também chamado NSS ou SS, seleciona o periférico e quase sempre é ativo em nível baixo. A cada pulso de clock sai um bit por MOSI e entra um bit por MISO ao mesmo tempo: o SPI é full-duplex, e para ler é preciso enviar alguma coisa (bytes \"dummy\") só para gerar o clock.\n\nModo: CPOL diz se o clock parado fica em 0 ou 1, e CPHA diz se o dado é lido na primeira ou na segunda borda; juntos formam os modos 0 a 3. Os dois lados precisam usar o mesmo modo, a mesma ordem de bits (quase sempre o mais significativo primeiro) e um clock que o periférico aceite. Não há endereço nem confirmação de recebimento: com o modo errado, os bytes chegam deslocados ou todos iguais (0x00 ou 0xFF), sem nenhum aviso de erro.\n\nVários periféricos compartilham SCK, MOSI e MISO, e cada um tem o seu CS; só o selecionado aciona MISO, os outros deixam a linha em alta impedância. CS por software (um GPIO comum) é o jeito mais flexível; o NSS por hardware do STM32 atende bem um único periférico. Para mais velocidade existem variantes com mais linhas de dados, Dual e Quad SPI (veja QSPI), usadas por memórias Flash.\n\nO STM32H743 tem seis SPI (SPI1 a SPI6), até 150 Mbit/s, quadros de 4 a 16 bits, FIFO, CRC por hardware e DMA; SPI1, SPI2 e SPI3 também fazem I2S (áudio), e o SPI6 fica no domínio D3, de baixo consumo. Com fios de protoboard, 1 a 10 MHz já é bastante; acima disso, fios curtos e um GND ao lado de cada sinal fazem diferença.",
      "example": "H743 WeAct: SPI2 livre nos headers em PB13 (SCK), PB14 (MISO), PB15 (MOSI) e PB12 (NSS) — os mesmos pinos que o TCC usa na BlackPill para o ADS1256. Na própria placa, a flash SPI de 8 MB está no SPI1 (PB3, PB4, PD7, CS em PD6) e o display no SPI4 (PE12 e PE14).",
      "figure": "assets/glossary/spi.svg",
      "figure_caption": "Barramento com um controlador e dois periféricos (SCK, MOSI e MISO compartilhados, um CS para cada), usando os pinos da Flash SPI da H743; embaixo, um byte trocado no modo 0 e a tabela dos quatro modos CPOL/CPHA.",
      "meaning": "Serial Peripheral Interface · interface periférica serial",
      "position": 7,
      "short": "Barramento síncrono de quatro fios (clock, dados de ida, dados de volta e seleção) em que o controlador gera o clock e fala com um periférico por vez: simples, rápido e full-duplex.",
      "term": "SPI"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "Taxa total do conversor não é necessariamente taxa por canal. Troca de canal e filtros também consomem tempo.",
      "example": "No sistema ADS1256, não divida a taxa nominal sem considerar a sequência de aquisição.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Samples Per Second · amostras por segundo",
      "position": 15,
      "short": "Taxa de produção de amostras.",
      "term": "SPS"
    },
    {
      "aliases": [],
      "category_id": "memoria",
      "detail": "Armazena variáveis, pilha e buffers. Bancos de SRAM podem ter acessos diferentes para CPU e DMA.",
      "example": "G474: 96 KiB de SRAM mais 32 KiB de CCM; F411: 128 KiB.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Static Random-Access Memory · memória estática de acesso aleatório",
      "position": 2,
      "short": "Memória de trabalho; perde os dados ao desligar.",
      "term": "SRAM"
    },
    {
      "aliases": [],
      "category_id": "gravacao",
      "detail": "Usa SWDIO e SWCLK, além da referência de terra e tensão; reset pode ajudar. O programa do gravador precisa reconhecer o chip.",
      "example": "ST-Link V2 atende às BluePill e BlackPill; H7RS requer verificar suporte atualizado.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Serial Wire Debug · depuração serial",
      "position": 1,
      "short": "Interface de gravação e depuração dos Arm.",
      "term": "SWD"
    },
    {
      "aliases": [],
      "category_id": "memoria",
      "detail": "ITCM guarda código e DTCM guarda dados críticos; o acesso não passa pelo barramento AXI. Confira quais controladores DMA alcançam cada banco antes de colocar buffers nela.",
      "example": "H743: 64 KiB de ITCM e 128 KiB de DTCM somados aos 864 KiB de SRAM.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Tightly-Coupled Memory · memória acoplada ao núcleo",
      "position": 6,
      "short": "RAM ligada diretamente ao Cortex-M7, sem cache e com tempo de acesso fixo.",
      "term": "TCM"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Para UART entre dois dispositivos, normalmente liga ao RX do outro. Confirme a perspectiva da rotulagem do adaptador.",
      "example": "TX do CH343P vai ao RX da placa.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Transmit · transmissão",
      "position": 18,
      "short": "Sinal de saída de dados seriais.",
      "term": "TX"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "Um prescaler divide o clock de entrada. O estouro ou comparação pode gerar interrupções. Watchdog é um temporizador de recuperação, não uma saída PWM.",
      "example": "PIC12F675 tem Timer0 de 8 bits e Timer1 de 16 bits.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Temporizador/contador",
      "position": 4,
      "short": "Conta ciclos ou eventos externos.",
      "term": "Timer"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "Não é limite garantido para todas as unidades. Para dimensionar margens use mínimo/máximo quando fornecidos.",
      "example": "Consumo típico muda com tensão, clock e temperatura.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Valor típico",
      "position": 10,
      "short": "Valor representativo em condições de teste.",
      "term": "Typical"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "Ligação ponto a ponto: o TX de um vai ao RX do outro, e os GND precisam estar ligados. A linha fica em 1 quando está ociosa; um byte começa com o start bit (0), segue com 5 a 9 bits de dados, do menos significativo para o mais significativo, um bit de paridade opcional e um ou dois stop bits (1). O formato é escrito como 8N1: 8 bits de dados, sem paridade, 1 stop bit.\n\nNão existe clock no fio. O receptor detecta a descida do start bit e, a partir dela, lê cada bit no meio do seu intervalo usando o próprio clock (o STM32 amostra 16 ou 8 vezes por bit). Por isso o baud rate precisa ser igual nos dois lados e a soma dos erros de clock deve ficar abaixo de cerca de 2 %: com cristal não há problema; com oscilador RC interno ou baud rate que não divide bem o clock do periférico surgem caracteres trocados e erros de quadro. A 115 200 bit/s cada bit dura 8,68 µs e um quadro 8N1 de 10 bits leva 86,8 µs (até 11 520 bytes/s).\n\nNível elétrico: a UART do microcontrolador trabalha em nível lógico (3,3 V no STM32, 5 V no Arduino Uno). RS-232 usa tensões de ±3 a ±15 V, invertidas, e queima o pino se ligado direto; precisa de um conversor como o MAX3232. RS-485 e LIN também exigem transceptor. Um adaptador USB–UART (CH343P, CH340, FT232) mostra a UART ao computador como porta COM, /dev/ttyUSB ou /dev/ttyACM.\n\nNa prática: receba por interrupção ou DMA para não perder bytes, trate o erro de overrun e use controle de fluxo RTS/CTS quando o outro lado for lento. Para vários dispositivos no mesmo par de fios, use RS-485 com DE (veja USART). O bootloader de fábrica do STM32 aceita gravação pela UART: no H743, USART1 em PA9/PA10 com BOOT0 em nível alto.",
      "example": "H743 WeAct: USART1 em PA9 (TX) e PA10 (RX), ligado ao CH343P do acervo para console e gravação pelo bootloader. No Arduino Uno e Nano, D0/D1 são a UART do ATmega328P, já usada pela ponte USB. O PIC16F887 usa a EUSART em RC6/RC7.",
      "figure": "assets/glossary/uart.svg",
      "figure_caption": "Ligação cruzada do CH343P ao USART1 da H743 (PA9/PA10), a forma de onda do byte 0x41 em 8N1 a 115 200 bit/s com os pontos de amostragem, a notação 8N1 e os erros mais comuns.",
      "meaning": "Universal Asynchronous Receiver/Transmitter · transmissor/receptor assíncrono universal",
      "position": 3,
      "short": "Comunicação serial por dois fios de dados (TX e RX) sem clock: os dois lados combinam antes a velocidade e o formato, e cada byte viaja num quadro com bit de início e bit de parada.",
      "term": "UART"
    },
    {
      "aliases": [],
      "category_id": "fisico",
      "detail": "A numeração é uma matriz de posições. Confira a orientação superior/inferior no desenho do fabricante.",
      "example": "STM32H7R3Z8J6 usa UFBGA de 144 contatos.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Ultra-thin Fine-pitch Ball Grid Array",
      "position": 7,
      "short": "Encapsulamento com esferas de contato por baixo.",
      "term": "UFBGA"
    },
    {
      "aliases": [],
      "category_id": "fisico",
      "detail": "A pinagem e pad central precisam seguir o desenho do fabricante. Não é intercambiável fisicamente com LQFP.",
      "example": "STM32G474CEU6 e STM32F411CEU6 usam UFQFPN de 48 pinos.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Ultra-thin Fine-pitch Quad Flat Package No-lead",
      "position": 6,
      "short": "Encapsulamento fino com contatos sem pernas expostas.",
      "term": "UFQFPN"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "No modo assíncrono o USART é exatamente uma UART: TX e RX com quadro start, dados, paridade e stop, e baud rate combinado entre os dois lados (veja UART). O \"S\" de síncrono acrescenta o pino CK: o USART gera um pulso de clock para cada bit e o outro lado lê os dados nesse ritmo, sem baud rate combinado. Na prática vira um SPI mestre simples (CK = SCK, TX = MOSI, RX = MISO).\n\nSinais extras opcionais: RTS/CTS fazem controle de fluxo por hardware. Quem recebe ativa RTS quando tem espaço e o outro lado só transmite com o seu CTS ativo, o que evita perder bytes com módulos lentos (Wi-Fi, Bluetooth, modems). DE (Driver Enable) liga o transmissor de um transceptor RS-485 só durante o envio, permitindo vários dispositivos no mesmo par de fios; no STM32 o pino RTS vira DE quando o modo RS-485 está ativo.\n\nO mesmo bloco ainda oferece half-duplex num fio só, LIN (redes automotivas), IrDA (infravermelho), Smartcard ISO 7816, detecção automática de baud rate, timeout de recepção (útil para Modbus) e modo multiprocessador. No STM32H743 cada USART tem FIFO de 16 posições na transmissão e na recepção, atende DMA, chega a 12,5 Mbit/s e tem clock independente da CPU: pode acordar o chip do modo Stop ao receber um start bit.\n\nO H743 tem quatro USART (1, 2, 3 e 6) e quatro UART (4, 5, 7 e 8). As UART não têm CK nem Smartcard, mas mantêm RTS/CTS, DE, LIN, IrDA e FIFO. Na HAL da ST, o modo síncrono usa as funções HAL_USART_* e o assíncrono (o mais comum) usa HAL_UART_*, inclusive nos USART. Cada sinal só existe em certos pinos, e o número da função alternativa muda de pino para pino: confira na pinagem completa.",
      "example": "H743 WeAct: USART3 completo e livre nos headers, com PD8 TX, PD9 RX, PD10 CK, PB13 CTS e PB14 RTS/DE. O USART1 em PA9/PA10 é o mesmo usado pelo bootloader serial (gravação com o CH343P). A BlackPill F411 tem USART1, 2 e 6.",
      "figure": "assets/glossary/usart.svg",
      "figure_caption": "Os quatro modos de ligação do USART3 da H743 (assíncrono, síncrono com CK, controle de fluxo RTS/CTS e RS-485 com DE), as diferenças entre USART e UART no H743 (DS12110, tabela 6) e os pinos livres na placa.",
      "meaning": "Universal Synchronous/Asynchronous Receiver/Transmitter · transmissor/receptor universal síncrono e assíncrono",
      "position": 4,
      "short": "Periférico serial que faz tudo o que uma UART faz e ainda pode enviar o próprio clock (modo síncrono), controlar o fluxo com RTS/CTS e acionar transceptores RS-485.",
      "term": "USART"
    },
    {
      "aliases": [],
      "category_id": "comunicacao",
      "detail": "A função pode ser dispositivo ou host. FS significa Full Speed (12 Mbit/s), HS High Speed (480 Mbit/s). O chip e a placa precisam oferecer o circuito necessário.",
      "example": "No Uno clássico a USB passa por uma ponte; no F411 o MCU possui USB nativa.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Universal Serial Bus · barramento serial universal",
      "position": 9,
      "short": "Interface de comunicação e alimentação.",
      "term": "USB"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "Normalmente usada para manter RTC e registros de backup. Não é a alimentação geral da placa.",
      "example": "Confira VBAT no pinout da BlackPill antes de ligar uma bateria.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Backup Battery supply",
      "position": 13,
      "short": "Alimentação do domínio de backup.",
      "term": "VBAT"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "A faixa de alimentação do chip é diferente da entrada VIN da placa. Consulte também limites por frequência e alimentação analógica VDDA.",
      "example": "USB de 5 V pode alimentar o regulador de uma placa STM32, mas seus GPIO operam em 3,3 V.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Tensão positiva de alimentação",
      "position": 1,
      "short": "Alimentação do microcontrolador.",
      "term": "VDD"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "Depende do tipo de entrada e alimentação. Compatibilidade exige que a saída do transmissor satisfaça este limite.",
      "example": "Uma saída de 3,3 V nem sempre satisfaz uma entrada de 5 V.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Voltage Input High",
      "position": 5,
      "short": "Menor tensão garantida como nível lógico alto.",
      "term": "VIH"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "Leia a coluna de condições. Uma entrada entre VIL máximo e VIH mínimo não tem estado lógico garantido.",
      "example": "Importante ao interligar dispositivos de 3,3 V e 5 V.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Voltage Input Low",
      "position": 4,
      "short": "Maior tensão garantida como nível lógico baixo.",
      "term": "VIL"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "A corrente fornecida pode reduzir a tensão. Não dimensione cargas só pelo limite máximo absoluto do pino.",
      "example": "VOH mínimo do transmissor precisa superar VIH mínimo do receptor.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Voltage Output High",
      "position": 7,
      "short": "Tensão de saída quando o pino produz nível alto.",
      "term": "VOH"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "O valor depende da corrente absorvida e da alimentação. A saída não é um curto ideal ao terra.",
      "example": "Confira a corrente de teste na tabela elétrica.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Voltage Output Low",
      "position": 6,
      "short": "Tensão de saída quando o pino produz nível baixo.",
      "term": "VOL"
    },
    {
      "aliases": [],
      "category_id": "analogico",
      "detail": "Ruído e erro da referência afetam a medição. Não confunda tensão máxima de alimentação com escala do ADC.",
      "example": "Escolha a referência antes de converter códigos ADC em volts.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Reference Voltage · tensão de referência",
      "position": 9,
      "short": "Referência que define a escala de um conversor.",
      "term": "VREF"
    },
    {
      "aliases": [],
      "category_id": "eletrica",
      "detail": "Normalmente ligada ao GND do circuito. O retorno e o desacoplamento influenciam a integridade dos sinais.",
      "example": "PIC usa VSS no datasheet; placas costumam rotular GND.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Referência negativa de alimentação",
      "position": 2,
      "short": "Referência de terra do chip.",
      "term": "VSS"
    },
    {
      "aliases": [],
      "category_id": "fundamentos",
      "detail": "Precisa ser atendido no prazo configurado. Não resolve toda falha e não deve ser alimentado indiscriminadamente.",
      "example": "PICs e STM32 incluem mecanismos watchdog.",
      "figure": null,
      "figure_caption": null,
      "meaning": "Temporizador de supervisão",
      "position": 14,
      "short": "Reinicia ou sinaliza se o software deixa de responder.",
      "term": "Watchdog"
    }
  ],
  "glossary_categories": [
    {
      "description": "Como o microcontrolador executa trabalho e como comparar sua capacidade sem confundir frequência, arquitetura e testes.",
      "icon": "◎",
      "id": "fundamentos",
      "name": "Processamento e desempenho",
      "position": 1,
      "tips": [
        "Compare números obtidos pelo mesmo método; MIPS, DMIPS e CoreMark usam escalas diferentes.",
        "Confirme se o recurso é do núcleo, de um periférico ou de um acelerador separado.",
        "Frequência máxima indica ritmo de clock, não garante sozinha menor tempo de execução."
      ]
    },
    {
      "description": "Onde programa e dados ficam guardados, o que se perde ao desligar e como o firmware começa a executar.",
      "icon": "▤",
      "id": "memoria",
      "name": "Memória e inicialização",
      "position": 2,
      "tips": [
        "Separe memória não volátil, que retém dados sem energia, da memória de trabalho volátil.",
        "Confira tamanho, endereço, resistência a escritas e quais controladores conseguem acessar cada banco.",
        "Reserve margem para pilha, buffers e atualizações; a capacidade anunciada não fica toda livre para a aplicação."
      ]
    },
    {
      "description": "Como tensões viram números, números viram sinais e temporizadores coordenam medições e acionamentos.",
      "icon": "∿",
      "id": "analogico",
      "name": "Analógico, tempo e controle",
      "position": 3,
      "tips": [
        "Resolução nominal não é o mesmo que precisão: referência, ruído, linearidade e tempo de aquisição também importam.",
        "Verifique se o canal chega ao pino da placa e se não conflita com outra função alternativa.",
        "Para cargas de potência, a saída do microcontrolador comanda um driver; ela não deve alimentar a carga diretamente."
      ]
    },
    {
      "description": "Como bits e sinais trafegam entre o microcontrolador, sensores, módulos e o computador.",
      "icon": "⇄",
      "id": "comunicacao",
      "name": "Pinos e comunicação",
      "position": 4,
      "tips": [
        "Antes de ligar, confirme tensão lógica, direção do sinal, referência GND e pinagem dos dois lados.",
        "Controlador interno, transceptor elétrico e conector físico são partes diferentes; a placa pode não incluir todas.",
        "Funções alternativas compartilham pinos, portanto nem todas as interfaces ficam disponíveis simultaneamente."
      ]
    },
    {
      "description": "Tensões, correntes, referências e condições que definem uma conexão segura e confiável.",
      "icon": "⚡",
      "id": "eletrica",
      "name": "Alimentação, clock e limites",
      "position": 5,
      "tips": [
        "Projete com as condições operacionais recomendadas; limite máximo absoluto é fronteira de dano, não ponto de trabalho.",
        "Leia sempre unidade, tensão de alimentação, temperatura e corrente usadas na medição da tabela.",
        "Terra comum é necessário para sinais referenciados, mas não corrige níveis lógicos incompatíveis."
      ]
    },
    {
      "description": "Como carregar firmware, escolher o modo de partida, reiniciar e investigar o programa em execução.",
      "icon": "⌁",
      "id": "gravacao",
      "name": "Gravação e depuração",
      "position": 6,
      "tips": [
        "Confirme família do chip, interface, tensão de referência e suporte do software antes de conectar o gravador.",
        "Bootloader ocupa ou redireciona parte da memória; o endereço da aplicação precisa corresponder ao método de inicialização.",
        "Bits de configuração podem alterar clock, proteção e reset; registre o estado antes de modificá-los."
      ]
    },
    {
      "description": "Como reconhecer o componente físico, orientar seus pinos e localizar a informação completa do fabricante.",
      "icon": "▦",
      "id": "fisico",
      "name": "Encapsulamento e documentos",
      "position": 7,
      "tips": [
        "Confirme código completo, encapsulamento, revisão da placa e orientação do pino 1.",
        "Pinout resume posições; datasheet define limites; manual de referência detalha registros e periféricos.",
        "O número de terminais do encapsulamento não equivale à quantidade de GPIO livres."
      ]
    }
  ],
  "movement_types": [
    {
      "action": "Comprei mais",
      "delta_in_use": 0,
      "delta_total": 1,
      "description": "Unidades novas entram como disponíveis.",
      "id": "compra",
      "label": "Compra",
      "position": 1,
      "tone": "green"
    },
    {
      "action": "Coloquei em uso",
      "delta_in_use": 1,
      "delta_total": 0,
      "description": "Unidades disponíveis passam a ficar ocupadas em um projeto.",
      "id": "uso",
      "label": "Em uso",
      "position": 2,
      "tone": "blue"
    },
    {
      "action": "Parei de usar",
      "delta_in_use": -1,
      "delta_total": 0,
      "description": "Unidades em uso voltam a ficar disponíveis.",
      "id": "devolucao",
      "label": "Liberada",
      "position": 3,
      "tone": "teal"
    },
    {
      "action": "Descartei (quebrou, perdi, doei)",
      "delta_in_use": 0,
      "delta_total": -1,
      "description": "Unidades disponíveis saem do acervo.",
      "id": "descarte",
      "label": "Descarte",
      "position": 4,
      "tone": "red"
    },
    {
      "action": "Descartei uma que estava em uso",
      "delta_in_use": -1,
      "delta_total": -1,
      "description": "Unidades que estavam em uso saem do acervo.",
      "id": "descarte_em_uso",
      "label": "Descarte em uso",
      "position": 5,
      "tone": "red"
    },
    {
      "action": "Entrada sem compra (contagem, presente)",
      "delta_in_use": 0,
      "delta_total": 1,
      "description": "Cadastro inicial ou unidades recebidas sem compra.",
      "id": "entrada",
      "label": "Entrada",
      "position": 6,
      "tone": "slate"
    }
  ],
  "pin_guides": [
    {
      "guide": "avr",
      "label": "Alimentação e referência",
      "position": 1,
      "term": "VDD"
    },
    {
      "guide": "avr",
      "label": "Pinos de entrada / saída",
      "position": 2,
      "term": "GPIO"
    },
    {
      "guide": "avr",
      "label": "Entradas analógicas",
      "position": 3,
      "term": "ADC"
    },
    {
      "guide": "avr",
      "label": "Comunicação serial",
      "position": 4,
      "term": "UART"
    },
    {
      "guide": "avr",
      "label": "Sinais SPI",
      "position": 5,
      "term": "SPI"
    },
    {
      "guide": "avr",
      "label": "Gravação / depuração",
      "position": 6,
      "term": "Bootloader"
    },
    {
      "guide": "pic",
      "label": "Alimentação e referência",
      "position": 1,
      "term": "VDD"
    },
    {
      "guide": "pic",
      "label": "Pinos de entrada / saída",
      "position": 2,
      "term": "GPIO"
    },
    {
      "guide": "pic",
      "label": "Entradas analógicas",
      "position": 3,
      "term": "ADC"
    },
    {
      "guide": "pic",
      "label": "Comunicação serial",
      "position": 4,
      "term": "UART"
    },
    {
      "guide": "pic",
      "label": "Sinais SPI",
      "position": 5,
      "term": "SPI"
    },
    {
      "guide": "pic",
      "label": "Gravação / depuração",
      "position": 6,
      "term": "ICSP"
    },
    {
      "guide": "pic12",
      "label": "1 · VDD",
      "position": 1,
      "term": "VDD"
    },
    {
      "guide": "pic12",
      "label": "2 · GP5 / RA5 · clock",
      "position": 2,
      "term": "Clock"
    },
    {
      "guide": "pic12",
      "label": "3 · GP4 / RA4 · analógico",
      "position": 3,
      "term": "ADC"
    },
    {
      "guide": "pic12",
      "label": "4 · GP3 / RA3 · MCLR / VPP",
      "position": 4,
      "term": "MCLR"
    },
    {
      "guide": "pic12",
      "label": "5 · GP2 / RA2 · funções alternativas",
      "position": 5,
      "term": "GPIO"
    },
    {
      "guide": "pic12",
      "label": "6 · GP1 / RA1 · ICSPCLK",
      "position": 6,
      "term": "ICSP"
    },
    {
      "guide": "pic12",
      "label": "7 · GP0 / RA0 · ICSPDAT",
      "position": 7,
      "term": "ICSP"
    },
    {
      "guide": "pic12",
      "label": "8 · VSS",
      "position": 8,
      "term": "VSS"
    },
    {
      "guide": "stm32",
      "label": "Alimentação e referência",
      "position": 1,
      "term": "VDD"
    },
    {
      "guide": "stm32",
      "label": "Pinos de entrada / saída",
      "position": 2,
      "term": "GPIO"
    },
    {
      "guide": "stm32",
      "label": "Entradas analógicas",
      "position": 3,
      "term": "ADC"
    },
    {
      "guide": "stm32",
      "label": "Comunicação serial",
      "position": 4,
      "term": "UART"
    },
    {
      "guide": "stm32",
      "label": "Sinais SPI",
      "position": 5,
      "term": "SPI"
    },
    {
      "guide": "stm32",
      "label": "Gravação / depuração",
      "position": 6,
      "term": "SWD"
    }
  ],
  "processing_classes": [
    {
      "name": "Essencial",
      "rank": 1
    },
    {
      "name": "Básico",
      "rank": 2
    },
    {
      "name": "Intermediário",
      "rank": 3
    },
    {
      "name": "Avançado",
      "rank": 4
    },
    {
      "name": "Avançado especializado",
      "rank": 5
    },
    {
      "name": "Alto desempenho",
      "rank": 6
    }
  ],
  "schema": 10,
  "sources": [
    {
      "file": "assets/documents/pic16f887.pdf",
      "retrieved": "2026-09-12",
      "sha256": "b032738ba2254371328908f1b7b19aec54be8dbbf112fbfc5032c3e7bf21ffa5",
      "url": "https://ww1.microchip.com/downloads/en/devicedoc/41291d.pdf"
    },
    {
      "file": "assets/documents/pic12f675.pdf",
      "retrieved": "2026-09-12",
      "sha256": "949b77de31b07295952ebac86ca0f303635a8ac595df991df8950f3518353cb2",
      "url": "https://ww1.microchip.com/downloads/en/devicedoc/41190c.pdf"
    },
    {
      "file": "assets/documents/pic12f683.pdf",
      "retrieved": "2026-09-12",
      "sha256": "8c33bd836b4623099d32059c436984918218d3788e8b3034df322cab1cffc1fb",
      "url": "https://ww1.microchip.com/downloads/en/devicedoc/41211d_.pdf"
    },
    {
      "file": "assets/documents/pic12f1501.pdf",
      "retrieved": "2026-09-12",
      "sha256": "9797df2bbfe0cc6ee78a1a7b2644ab1ff5b96bf6617b2ef600b3d5f3b5540f52",
      "url": "https://ww1.microchip.com/downloads/aemDocuments/documents/OTH/ProductDocuments/DataSheets/40001615C.pdf"
    },
    {
      "file": "assets/documents/atmega328p.pdf",
      "retrieved": "2026-09-12",
      "sha256": "fb84858d0b12c695a12b13f0c74b962d81210247d440c7a24c0ed23dfabfdfaf",
      "url": "https://docs.arduino.cc/resources/datasheets/ATmega328P-datasheet.pdf"
    },
    {
      "file": "assets/documents/uno-pinout.pdf",
      "retrieved": "2026-09-12",
      "sha256": "088b4d7d776abf443cb050c31875221aa5fc7f0533470b33e035c249cf240007",
      "url": "https://docs.arduino.cc/resources/pinouts/A000066-full-pinout.pdf"
    },
    {
      "file": "assets/documents/nano-pinout.pdf",
      "retrieved": "2026-09-12",
      "sha256": "2b9140b09cb66c788c1c4e01da33498a63e245fc133ac7d32697e140b00ea317",
      "url": "https://docs.arduino.cc/resources/pinouts/A000005-full-pinout.pdf"
    },
    {
      "file": "assets/documents/stm32f103c8.pdf",
      "retrieved": "2026-09-12",
      "sha256": "4741c03c5793745c1709ab48237ea23d204c4fc2ca735ceafa03367f32960917",
      "url": "https://raw.githubusercontent.com/WeActStudio/BluePill-Plus/master/Doc/STM32F103C8T6/DS5319-STM32F103x8-Datasheet.pdf"
    },
    {
      "file": "assets/documents/stm32g474.pdf",
      "retrieved": "2026-09-12",
      "sha256": "b018e20dbe34b63a43e49365518b186ef0e0e8e899deeabc1c9f53a3a10c1add",
      "url": "https://raw.githubusercontent.com/WeActStudio/WeActStudio.STM32G474CoreBoard/master/Doc/STM32G474xE_DS12288.pdf"
    },
    {
      "file": "assets/documents/g474-long-schematic.pdf",
      "retrieved": "2026-09-12",
      "sha256": "c8c5670359ae1a3d2ec069fc46d950722dc5a0e2a704621dc8c45fb1dcf9098b",
      "url": "https://raw.githubusercontent.com/WeActStudio/WeActStudio.STM32G474CoreBoard/master/Hardware/QFN48/WeAct-STM32G474CoreBoard_Long/WeAct-STM32G474CoreBoard_Long_V10 SchDoc.pdf"
    },
    {
      "file": "assets/documents/g474-long-pinout.pdf",
      "retrieved": "2026-09-12",
      "sha256": "37994a0bbb081bd81a57b95fcb0b9f2a785883866d32cb8cc740b04957e113b4",
      "url": "https://raw.githubusercontent.com/WeActStudio/WeActStudio.STM32G474CoreBoard/master/Hardware/QFN48/WeAct-STM32G474CoreBoard_Long/WeAct-STM32G474CoreBoard_Long_V10 Board Shape 外形.pdf"
    },
    {
      "file": "assets/documents/stm32h7r3.pdf",
      "retrieved": "2026-09-12",
      "sha256": "f818b9d0f5f67e1a25cb4f1316901d527a5e46fdfbe3a16d4de729bf42ba3483",
      "url": "https://raw.githubusercontent.com/WeActStudio/WeActStudio.STM32H7R3Zx_CoreBoard/master/Doc/stm32h7r3z8.pdf"
    },
    {
      "file": "assets/documents/h7-schematic.pdf",
      "retrieved": "2026-09-12",
      "sha256": "f2d705a81600ad28647ab21ec339b6fade74ffd5b1f2a3be84231958b1d3c76e",
      "url": "https://raw.githubusercontent.com/WeActStudio/WeActStudio.STM32H7R3Zx_CoreBoard/master/Hardware/WeAct-STM32H7R3Zx_CoreBoard_V10 SchDoc.pdf"
    },
    {
      "file": "assets/documents/h7-pinout.pdf",
      "retrieved": "2026-09-12",
      "sha256": "10887ffec60e3ecfff3eda2dadca7146414f34752f1ec1ac07a2931ff3327c83",
      "url": "https://raw.githubusercontent.com/WeActStudio/WeActStudio.STM32H7R3Zx_CoreBoard/master/Hardware/WeAct-STM32H7R3Zx_CoreBoard_V10 Board Shape 外形.pdf"
    },
    {
      "file": "assets/documents/stm32f411ce.pdf",
      "retrieved": "2026-09-12",
      "sha256": "64b60c709aeafcc0cca3874ffeae4d1cc09ec752d1316e87c36c23f0e96686cc",
      "url": "https://raw.githubusercontent.com/WeActStudio/WeActStudio.MiniSTM32F4x1/master/Datasheet/STM32F411CEU6_Datasheet.pdf"
    },
    {
      "file": "assets/documents/blackpill-pinout.pdf",
      "retrieved": "2026-09-12",
      "sha256": "9b1a3b36a803108411bea313dd76947c3d5829927ee133d0dc17fdd55609d1d8",
      "url": "https://raw.githubusercontent.com/WeActStudio/WeActStudio.MiniSTM32F4x1/master/General document/STM32F4x1 v2.0+ Pin Layout.pdf"
    },
    {
      "file": "assets/documents/stm32h743vi.pdf",
      "retrieved": "2026-09-17",
      "sha256": "9c74d2015445f7c3c2c9076fc13a2665c8f6fecec7898d128dac836d6d39314b",
      "url": "https://raw.githubusercontent.com/WeActStudio/MiniSTM32H7xx/master/Datasheet/MCU/STM32H743VI_Datasheet.pdf"
    },
    {
      "file": "assets/documents/h743-schematic.pdf",
      "retrieved": "2026-09-17",
      "sha256": "cd0c19625e3d9e56b59368affb5ba8d89aeb5ab63c5320e6220500fc0b6502f2",
      "url": "https://raw.githubusercontent.com/WeActStudio/MiniSTM32H7xx/master/Hardware/STM32H7xx SchDoc V12.pdf"
    },
    {
      "file": "assets/documents/h743-pinout.pdf",
      "retrieved": "2026-09-17",
      "sha256": "222eb3b6b193e9a1deb30acb06c254adc029a6bcf43aaa79a03d0db99fa6a7fb",
      "url": "https://raw.githubusercontent.com/WeActStudio/MiniSTM32H7xx/master/Hardware/STM32H7xx_BoardShape Board Shape 外形 V12.pdf"
    }
  ],
  "spec_fields": [
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "variant",
      "label": "Variante da placa",
      "position": 1
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "cpu",
      "label": "CPU",
      "position": 2
    },
    {
      "format": "mhz",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "clock",
      "label": "Clock máximo",
      "position": 3
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "oscillator",
      "label": "Oscilador da placa / chip",
      "position": 4
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "flash",
      "label": "Flash interna",
      "position": 5
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "external",
      "label": "Flash externa",
      "position": 6
    },
    {
      "format": "bytes",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "ram",
      "label": "SRAM",
      "position": 7
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "eeprom",
      "label": "EEPROM / HEF",
      "position": 8
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "package",
      "label": "Encapsulamento",
      "position": 9
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "gpio",
      "label": "GPIO",
      "position": 10
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "adc",
      "label": "ADC",
      "position": 11
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "dac",
      "label": "DAC",
      "position": 12
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "pwm",
      "label": "PWM",
      "position": 13
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "timers",
      "label": "Timer",
      "position": 14
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "serial",
      "label": "Comunicação",
      "position": 15
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "voltage",
      "label": "Lógica / alimentação de referência",
      "position": 16
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "temperature",
      "label": "Temperatura",
      "position": 17
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "programmer",
      "label": "Gravação",
      "position": 18
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 1,
      "key": "special",
      "label": "Outros recursos",
      "position": 19
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 0,
      "key": "use",
      "label": "Aplicações",
      "position": 20
    },
    {
      "format": "text",
      "in_compare": 1,
      "in_sheet": 0,
      "key": "notes",
      "label": "Observações",
      "position": 21
    }
  ],
  "table_columns": [
    {
      "digits": null,
      "field": null,
      "format": "component",
      "group_id": "acervo",
      "help": null,
      "key": "name",
      "label": "Componente",
      "position": 1,
      "term": null,
      "unit": null,
      "width": 270
    },
    {
      "digits": null,
      "field": null,
      "format": "family",
      "group_id": "acervo",
      "help": null,
      "key": "family",
      "label": "Família",
      "position": 2,
      "term": null,
      "unit": null,
      "width": 90
    },
    {
      "digits": null,
      "field": null,
      "format": "stock",
      "group_id": "acervo",
      "help": "Unidades disponíveis / total no acervo. Registre compras, uso e descartes na aba Histórico.",
      "key": "stock",
      "label": "Disponível / total",
      "position": 3,
      "term": null,
      "unit": null,
      "width": 130
    },
    {
      "digits": null,
      "field": null,
      "format": "class",
      "group_id": "desempenho",
      "help": null,
      "key": "processing_class",
      "label": "Classe de processamento",
      "position": 4,
      "term": null,
      "unit": null,
      "width": 178
    },
    {
      "digits": 0,
      "field": null,
      "format": "metric",
      "group_id": "desempenho",
      "help": "Milhões de instruções por segundo. Usado aqui somente para PIC e ATmega328P.",
      "key": "mips_peak",
      "label": "Pico MIPS",
      "position": 5,
      "term": "MIPS",
      "unit": "MIPS",
      "width": 144
    },
    {
      "digits": null,
      "field": null,
      "format": "metric",
      "group_id": "desempenho",
      "help": "Pontuação do benchmark CoreMark. Maior é melhor.",
      "key": "coremark",
      "label": "CoreMark",
      "position": 6,
      "term": "CoreMark",
      "unit": null,
      "width": 144
    },
    {
      "digits": 2,
      "field": null,
      "format": "metric",
      "group_id": "desempenho",
      "help": "CoreMark dividido pela frequência em megahertz.",
      "key": "coremark_per_mhz",
      "label": "CoreMark/MHz",
      "position": 7,
      "term": "CoreMark",
      "unit": null,
      "width": 167
    },
    {
      "digits": 0,
      "field": null,
      "format": "metric",
      "group_id": "desempenho",
      "help": "Resultado do benchmark Dhrystone. Maior é melhor.",
      "key": "dmips",
      "label": "DMIPS",
      "position": 8,
      "term": "DMIPS",
      "unit": null,
      "width": 121
    },
    {
      "digits": 2,
      "field": null,
      "format": "metric",
      "group_id": "desempenho",
      "help": "DMIPS dividido pela frequência em megahertz.",
      "key": "dmips_per_mhz",
      "label": "DMIPS/MHz",
      "position": 9,
      "term": "DMIPS",
      "unit": null,
      "width": 144
    },
    {
      "digits": 2,
      "field": null,
      "format": "metric",
      "group_id": "desempenho",
      "help": "DMIPS do componente dividido pelos 90 DMIPS da BluePill.",
      "key": "relative_bluepill",
      "label": "Relativo à BluePill",
      "position": 10,
      "term": null,
      "unit": "×",
      "width": 178
    },
    {
      "digits": null,
      "field": null,
      "format": "annotated",
      "group_id": "desempenho",
      "help": null,
      "key": "accelerators",
      "label": "Aceleradores",
      "position": 11,
      "term": null,
      "unit": null,
      "width": 253
    },
    {
      "digits": null,
      "field": null,
      "format": "text",
      "group_id": "desempenho",
      "help": null,
      "key": "cpu",
      "label": "Núcleo / recursos",
      "position": 12,
      "term": "CPU",
      "unit": null,
      "width": 218
    },
    {
      "digits": null,
      "field": null,
      "format": "mhz",
      "group_id": "desempenho",
      "help": null,
      "key": "clock",
      "label": "Clock",
      "position": 13,
      "term": "Clock",
      "unit": null,
      "width": 106
    },
    {
      "digits": null,
      "field": "flash_short",
      "format": "annotated",
      "group_id": "desempenho",
      "help": null,
      "key": "flash",
      "label": "Flash",
      "position": 14,
      "term": "Flash",
      "unit": null,
      "width": 121
    },
    {
      "digits": null,
      "field": null,
      "format": "bytes",
      "group_id": "desempenho",
      "help": null,
      "key": "ram",
      "label": "SRAM",
      "position": 15,
      "term": "SRAM",
      "unit": null,
      "width": 121
    },
    {
      "digits": null,
      "field": null,
      "format": "annotated",
      "group_id": "desempenho",
      "help": null,
      "key": "eeprom",
      "label": "EEPROM / HEF",
      "position": 16,
      "term": "EEPROM",
      "unit": null,
      "width": 167
    },
    {
      "digits": null,
      "field": null,
      "format": "annotated",
      "group_id": "perifericos",
      "help": null,
      "key": "gpio",
      "label": "GPIO",
      "position": 17,
      "term": "GPIO",
      "unit": null,
      "width": 201
    },
    {
      "digits": null,
      "field": null,
      "format": "annotated",
      "group_id": "perifericos",
      "help": null,
      "key": "adc",
      "label": "ADC",
      "position": 18,
      "term": "ADC",
      "unit": null,
      "width": 213
    },
    {
      "digits": null,
      "field": null,
      "format": "annotated",
      "group_id": "perifericos",
      "help": null,
      "key": "dac",
      "label": "DAC",
      "position": 19,
      "term": "DAC",
      "unit": null,
      "width": 173
    },
    {
      "digits": null,
      "field": null,
      "format": "annotated",
      "group_id": "perifericos",
      "help": null,
      "key": "pwm",
      "label": "PWM",
      "position": 20,
      "term": "PWM",
      "unit": null,
      "width": 201
    },
    {
      "digits": null,
      "field": null,
      "format": "annotated",
      "group_id": "perifericos",
      "help": null,
      "key": "timers",
      "label": "Temporizadores",
      "position": 21,
      "term": "Timer",
      "unit": null,
      "width": 242
    },
    {
      "digits": null,
      "field": null,
      "format": "annotated",
      "group_id": "perifericos",
      "help": null,
      "key": "serial",
      "label": "Comunicação",
      "position": 22,
      "term": null,
      "unit": null,
      "width": 282
    },
    {
      "digits": null,
      "field": null,
      "format": "text",
      "group_id": "eletrica",
      "help": null,
      "key": "voltage",
      "label": "Lógica",
      "position": 23,
      "term": null,
      "unit": null,
      "width": 115
    }
  ],
  "tools": [
    {
      "compatibility": "UART de STM32 quando o bootloader do modelo permite. Conferir nível lógico do módulo; ligar TX→RX, RX→TX e GND. Não fornece SWD.",
      "description": "Ponte USB–UART: permite comunicação serial com o computador. Não é depurador.",
      "id": "ch343p",
      "name": "CH343P",
      "quantity": 1
    },
    {
      "compatibility": "BluePill F103, BlackPill F411 e H743 via SWD. G474 requer software atualizado; conferir suporte H7RS para H7R3 e variante/firmware do gravador.",
      "description": "Programador e depurador: grava firmware e permite inspecionar execução.",
      "id": "stlink",
      "name": "ST-Link V2",
      "quantity": 1
    },
    {
      "compatibility": "PIC16F887, PIC12F675, PIC12F683 e PIC12F1501 via ICSP, com versão de software que liste o dispositivo. Depuração pode exigir recursos adicionais; não serve como gravador AVR do Arduino.",
      "description": "Programador e depurador de microcontroladores Microchip. Nome informado como “picokit 3”.",
      "id": "pickit",
      "name": "PICkit 3",
      "quantity": 1
    }
  ]
};
