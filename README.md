cocoapods-graph
================

This tool generates a dependencies graph report, printing on console or saving on a json or creating a html with a interactive disc to navigate through it.

## Example for Wordpress iOS app dependencies <a href="https://github.com/wordpress-mobile/WordPress-iOS">link</a> ##


![the dependency wheel for wordpress iOS app](https://github.com/erickjung/cocoapods-graph/blob/master/docs/wordpress_example.gif)

## Installing ##
```shell
[sudo] pip install cocoapods-graph
```

## How to use ##
```shell
cocoapods-graph -f Podfile.lock --html
```

## Thanks ##

All html rendering is done with:
* <a href="https://github.com/mbostock/d3">d3.js</a>
* <a href="https://github.com/fzaninotto/DependencyWheel">Dependency Wheel</a>

