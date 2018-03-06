# econ-graphing

Providing an easy way for high school students studying economics to create nice-looking graphs

## Intro

This is a very simple codebase that makes it possible for high school economics students with limited or no coding knowledge to be able to create graphs of an economic model.  The capabilities include labelled and coloured lines, intersections with labels, points on the axes, shading and annotations.  In short, about all that is needed for relatively simple graphs of an application of the economic model.  

Designed with the microeconomic model in mind, the flexibility of the code allows for this to be used for macroeconomic models as well.  

## Thanks to Plot.ly

The graphs are made using [plot.ly](https://plot.ly "Plot.ly: Modern Visualization for the Data Era") which makes doing this kind of work a breeze and very enjoyable.  


## Graphs are defined using YAML

A graph is defined using YAML, as shown in the example below:

```yaml
title: Example Graph
configuration:
    x_title: Quantity of widgets
    y_title: Price of widgets in $
lines:
  demand:
    color: CadetBlue
    el: -1.5
    label: D
    left_point: [15, 60]
  supply:
    color: SeaGreen
    el: 1.5
    label: S
    left_point: [15, 5]

intersections:
  supply-and-demand:
    line1: supply
    line2: demand
    x-axis-label: Qeq
    y-axis-label: Peq
    color: Plum
```

![Alt text](docs/plot.png?raw=true "Simple example")

Other sections are `Shading` and `Annotations`. 


### Rules

#### Permissions

* `commercial-use` - This software and derivatives may be used for commercial purposes.
* `modifications` - This software may be modified.
* `distribution` - This software may be distributed.
* `private-use` - This software may be used and modified in private.
* `patent-use` - This license provides an express grant of patent rights from contributors.

#### Conditions

* `include-copyright` - A copy of the license and copyright notice must be included with the software.
* `document-changes` - Changes made to the code must be documented.
* `disclose-source` - Source code must be made available when the software is distributed.
* `network-use-disclose` - Users who interact with the software via network are given the right to receive a copy of the source code.
* `same-license` - Modifications must be released under the same license when distributing the software. In some cases a similar or related license may be used.
* `same-license--file` - Modifications of existing files must be released under the same license when distributing the software. In some cases a similar or related license may be used.
* `same-license--library` - Modifications must be released under the same license when distributing the software. In some cases a similar or related license may be used, or this condition may not apply to works that use the software as a library.

#### Limitations

* `trademark-use` - This license explicitly states that it does NOT grant trademark rights, even though licenses without such a statement probably do not grant any implicit trademark rights.
* `liability` - This license includes a limitation of liability.
* `patent-use` - This license explicitly states that it does NOT grant any rights in the patents of contributors.
* `warranty` - The license explicitly states that it does NOT provide any warranty.

## License

The content of this project itself is licensed under the [Creative Commons Attribution 3.0 license](http://creativecommons.org/licenses/by/3.0/us/deed.en_US).