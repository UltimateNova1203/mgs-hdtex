## QAR Format

Below is a breakdown of the QAR container format. The container is a concatenation of the XTI files, followed by a footer that describes what the container holds, and other various info.

### Footer of .\cdrom.img\face\f01b\face.qar

<pre>
04 = Number of mega-textures in container (4) 
   00 
      00 = XTI Texture 1 Data Start 
         00 
            07 F0 15 = XTI Texture 1 Pointer Name 
                     17 = End of Texture 
                        80 0A 03 = XTI Texture 2 Data Start 
                                 00 
                                    EA 4C A8 = XTI Texture 2 Pointer Name 
                                             17 = End of Texture 
 
00 5F 03 = XTI Texture 3 Data Start 
         00 
            0A 50 F2 = XTI Texture 3 Pointer Name 
                     17 = End of Texture 
                        80 5C 04 = XTI Texture 4 Data Start 
                                 00 
                                    D4 EE 9D = XTI Texture 4 Pointer Name 
                                             17 = End of Texture 
 

80 A6 01 = XTI Texture File Names Start 
         00 
            63 61 6D 5F 72 61 64 69 6F 5F 6D 68 

5F 6D 74 2E 78 74 69 = XTI Texture 1 File Name (cam_radio_mh_mt.xti) 
                     00 
                        72 61 69 5F 72 61 64 69 

6F 5F 64 69 76 65 72 5F 6D 68 5F 6D 74 2E 78 74 

69 = XTI Texture 2 File Name (rai_radio_diver_mh_mt.xti) 
   00 
      72 6F 73 5F 72 61 64 69 6F 5F 6D 68 5F 6D 

74 2E 78 74 69 = XTI Texture 3 File Name (ros_radio_mh_mt.xti) 
               00 
                  73 61 76 65 5F 6C 6F 61 64 2E 

78 74 69 = XTI Texture 4 File Name (save_load.xti) 
         00 
            80 6C 0C = Footer Data Start 
                     00 
 

</pre>
## XTI Format

Below is a breakdown of the XTI texture format. It is a DXT5-like texture sheet (hence forth called Mega-Texture), filled with multiple sub-textures that apply to the same models/assets.

### Header of .\cdrom.img\face\f01b\face.qar\save_load.xti

<pre>
00 00 00 00 04 00 00 00 01 00 00 00 
                                    50 06 00 00 = mega-texture metadata start (0x000650) 

0B 00 = number of textures in mega-texture (16bit, 11) 
      00 00 00 00 00 00 
                        80 06 00 00 = mega-texture data start (0x000680) 
                                    00 00 00 00 
 
 
00 00 = Height Offset (16bit, 0px) 
      00 3A 00 00 00 3A 00 80 FF 3E 00 00 6C 3D 

3F 53 E8 00 = Texture 1 Pointer Name 
            00 00 00 00 
                        00 03 = Texture Type (0003 is Alpha, 0000 has no Alpha) 
                              00 00 00 00 00 00 

42 00 00 00 00 00 00 00 42 00 00 00 00 00 00 00 

0A C0 7F 00 EC 00 00 00 08 00 00 00 00 00 00 00 

00 00 30 01 00 00 00 80 16 00 00 00 00 00 00 00 

00 00 04 A8 06 00 00 00 06 00 00 00 00 00 00 00 

00 80 FF 3E 00 00 6C 3D 00 00 80 3F 00 00 80 3F 

00 00 00 3A 00 00 00 3A 00 00 00 00 00 00 00 00 

00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 



14 00 00 00 
            00 04 = mega-texture width (24bit, 1024px) 
                  00 04 = mega-texture height (24bit, 1024px) 
                        01 00 = quadrant size?? (16bit, 256px) 
                              00 00 
                                    00 A0 01 00 = mega-texture size (32bit, 106,496 Bytes) 

80 06 00 00 = mega-texture data start (0x000680) 
            00 00 00 00 00 00 00 00 00 00 00 00 

00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
 
 
mega-texture used height is found by dividing size by width (106,496 B / 1024px = 104px 
</pre>