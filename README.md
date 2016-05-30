# Colorful
Colorful is a small python application used to extract color palettes from images and then compile configuration files for other applications using those palettes.

## Example configuration

Each retheming module consists of two configuration files. The initial configuration file is located in the `colorful/config`. The second is the "layout" file and is located wherever you specify inside of the initial configuration file.

```
# colorful/config/konsole.conf
[Application]
conf = /home/user/.local/share/konsole/Colorful.colorscheme
layout = /home/user/.config/colorful/layouts/konsole
format = rgb
```

The layout file will look something like this, depending on the application you are configuring.
```
# /home/user/.config/colorful/layouts/konsole
[Background]
Color = %0
[BackgroundIntense]
Color = %1
```

The output from `\%%d` is going to correspond to the canonical colors normally associated with default terminal colors.
Another more finicky output is currently processed: `\%p%d` (eg `%p5`). This will select colors based on "prominence". Rather than matching it to a specific color palette it is simply a list of colors within the image ordered by saturation and restricted to values where `0.2 < saturation < 0.9`.

*Currently the hex format compiles to `%0 => #rrggbb`, but will soon expect you to provide the `#` to make output more configurable (eg `#%0`).


