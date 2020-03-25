# edge-detection-coloring
## *Detecting and coloring edges according to their direction using NxN kernel convolutions' implementation.*

### Contents
[**Examples**](#examples)  
[**Kernel convolutions' implementation**](#kernel-convolutions-implementation)  
[**Usage**](#usage)  


### Examples

Input | Long Flags | Short Flags | Output
---|---|---|---
<img src="https://i.imgur.com/pUIL3IV.png" height="250"/>|<br/>|<br/>| <img src="https://i.imgur.com/cvPnJsm.png" height="250"  />
<img src="https://i.imgur.com/pUIL3IV.png" height="250"/>|**--colored**<br/>**--threshold 9 22**|**-c**<br/>**-t 9 22**| <img src="https://i.imgur.com/Q3vTRZl.png" height="250"  />
<img src="https://i.imgur.com/pUIL3IV.png" height="250"/>|**--colored**<br/>**--threshold 9 22**<br/>**--stroke 1**|**-c**<br/>**-t 9 22**<br/>**-s 1**| <img src="https://i.imgur.com/wxHrHMX.png" height="250"  />
<img src="https://i.imgur.com/pUIL3IV.png" height="250"/>|**--threshold 9 22**|**-t 9 22**| <img src="https://i.imgur.com/HqDk2Xr.png" height="250"  />

### Kernel convolutions' implementation

Instead of padding the image with black pixels i'm cropping the kernel to fit available pixels.

*For example:*

Given a kernel of 5x5 dimensions, on the first pixel (0, 0) theres no pixels before it to accommodate the kernel thus it is cropped for only available pixels and applied for the (0,0) pixel.
  <br/>
  <br/>
  <img src="https://i.imgur.com/eeh4VpG.png" height="150"  />
    **+**
  <img src="https://i.imgur.com/oqzEYbh.png" height="150"  />
   **->**
  <img src="https://i.imgur.com/gYej4ei.png" height="150"  />
  
### Usage

#### Launching
```
git clone https://github.com/MingaudasVagonis/edge-detection-coloring.git
cd edge-detection-coloring
python3 main.py [filename] [flags]
````
#### Flags

Long Flags | Short Flags | Description
---|---|---
--threshold | -t | One or two numbers representing lower and upper thresholds.
--colored | -c | Set this in order to apply color to the edges according to their direction.
--stroke | -s | A number representing the width of the output edge.
