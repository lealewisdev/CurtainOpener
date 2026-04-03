# Smart Home CurtainOpener

Features
- Command manually via integrated buttons
- Command remotely via Homeassistant MQTT integration
- Schedule automated opening via integrated buttons
- Retains status in case of power off
- Integrated StallGuard

Prerequisites
- [Mosquitto MQTT Broker](https://mosquitto.org/)
- [Homeassistant](https://www.home-assistant.io/) with [MQTT integration](https://www.home-assistant.io/integrations/mqtt/)

Parts List
- [Adafruit ESP32-S3 Reverse TFT Feather](https://thepihut.com/products/adafruit-esp32-s3-reverse-tft-feather-4mb-flash-2mb-psram-stemma-qt)
- [Adafruit TMC2209 Stepper Motor Driver Breakout Board](https://thepihut.com/products/adafruit-tmc2209-stepper-motor-driver-breakout-board)
- [Nema 17 17HS4401](https://www.aliexpress.com/item/1005008459399126.html?spm=a2g0o.order_detail.order_detail_item.2.160af19cnBNuYQ)
- [Solid Core Prototyping Wires](https://thepihut.com/products/prototyping-wire-spool-set) OR ([Jumper Cables  / Dupont Wires](https://thepihut.com/products/thepihuts-jumper-bumper-pack-120pcs-dupont-wire) AND [Breadboard](https://thepihut.com/products/raspberry-pi-breadboard-half-size))
- [USB C Plug](https://www.amazon.co.uk/Anker-Charger-PowerPort-iPhone-Included-White/dp/B095GNGP6S?crid=3LHF4UYW0YYMK&dib=eyJ2IjoiMSJ9.uD0rcrSb1uyc1uYUMAlSiq7p-eWvnTO-oVc6EJITdG7wxdA5usN00Y9AKRV96qLpurv_Z1q8OHco3M6ntI_QBumK3EC6tVyv4Mzncls5hmTNp7yM_CijsLpFj-9h6TiygldKR3PtN98CgP_GGhjVP0tUlRV58Il5rTHyVxrrJgpX3wWke-eXtti5qXPs9RGHQ3KGRX0Faat7nfkv9DTNZ1o-m8ZrDcXris_sfnv7Iv0.FHjK6gTjE-_b_wP8tGi7ifpo0ibLcxAjbaxT4eovN2Y&dib_tag=se&keywords=anker%2Busb%2Bc%2Bwall%2Bplug&qid=1775219334&sprefix=anker%2Busb%2Bc%2Bwall%2Caps%2C293&sr=8-1&th=1) AND [USB Socket Breakout](https://thepihut.com/products/simple-usb-c-socket-breakout) (OR [5V Power Supply](https://thepihut.com/products/3-12v-universal-power-supply-with-connectors-aps-1500) AND [Breadboard DC Barrel Jack](https://thepihut.com/products/breadboard-friendly-2-1mm-dc-barrel-jack))
- If soldering Headers and Connections: Soldering Iron + Solder


Instructions
- If neccessary: Flash Microcontroller with latest Bootloader and Firmware
- Clone repository onto Microcontroller
- Rename 'settings.toml.example' to 'settings.toml' and insert your Wifi and MQTT credentials
- Connect Microcontroller, Driver, Motor and Power Supply according to the [instructions provided by adafruit](https://learn.adafruit.com/adafruit-tmc2209-stepper-motor-driver-breakout-board/circuitpython-and-python)
- Configure the Homeassistant MQTT integration with the topic 'curtain', payloads 'OPEN' and 'CLOSE' as well as the states 'OPENED' and 'CLOSED'
