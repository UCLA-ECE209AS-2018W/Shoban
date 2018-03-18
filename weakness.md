---
layout: default
title: Limitations
description: Limitations
---

# Limitations of this attack:

* Following are the limitations with respect to the feasibility and accuracy of the demonstrated attack.
   - Some of the Smart phone manufacturers such as Lenovo, MI, Google Nexus and other Chinese brands do not support MHL or HDMI facility as they provide wireless screen mirroring facility. Since they provide wireless screen sharing they do not offer hardwired cable based screen sharing, which restricts the attack from being possible with the phones from above manufacturers. [The list of MHL compatible phone brands and models can be found here.](http://www.mhltech.org/devices.aspx) 
   - Some mobile phones from Samsung such as Galaxy S5 detect the recording and give a momentary notice to the users saying HDMI cable connected, which if detected this attack would fail.
   - The technique used to detect the characters pressed in this attack (Template matching) works best only with the standard qwerty keyboard. With variations in the keyboard and fonts the accuracy in detecting the characters pressed reduces.
* This attack can steal the phone unlock passwords, App passwords and other private information’s such as pictures, email messages. However extracting the passwords of email or other web services may not be feasible as they will be auto saved by the user in most cases.
* This attack can only detect the characters pressed in the first page of the standard qwerty keyboard as it has been trained only with the reference templates pertaining to the first page of the keyboard.
