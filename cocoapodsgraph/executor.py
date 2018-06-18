# Copyright (c) 2018 Erick Jung

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import sys
import json
from optparse import OptionParser

__version__ = "0.1.1"

PROJECT_NAME = "cocoapods-graph"
PROJECT_DESCRIPTION = "cocoapods dependencies graph generator"
PROJECT_AUTHOR = "erick jung (erickjung@gmail.com)"

class PodClass:
    name = ''
    version = ''
    dependencies = []

    def __init__(self, name, version, dependencies):
        self.name = name
        self.version = version
        self.dependencies = dependencies

    def printObject(self):
        print self.name + " " + self.version
        for dep in self.dependencies:
            print "  " + dep.name + " " + dep.version

# ---------

def parse_lock_file(fileName):
    def parse_lock_pods_line(line):
        try:
            name = line[line.index("-")+1:line.index("(")].strip()
        except Exception:
            name = line[line.index("-")+1:].strip()

        try:
            version = line[line.index("(")+1:line.index(")")].strip()
        except Exception:
            version = ""

        return PodClass(name, version, []) 

    with open(fileName, 'r+') as inFile:  
        contentFile = [x.replace('\n', '').replace('"', '') for x in inFile.readlines()] 

    resultList = []
    pod = PodClass("", "", [])
    for line in contentFile:
        if line.startswith('  -'):
            if len(pod.name) > 0:
                resultList.append(pod)
            pod = parse_lock_pods_line(line)
        elif line.startswith('    -'):
            pod.dependencies.append(parse_lock_pods_line(line))
        elif line.startswith('DEPENDENCIES'):
            break
            
    return resultList


def generate_json(resultList):
    def generate_json_deps(resultList):
        data = '{'
        for result in resultList:
            data += '"%s":"%s",' % (result.name, result.version)

        data = data[:len(data)-1]    
        return data + '}'
        
    json = '{"packages": ['
    deps = generate_json_deps(resultList)
    json += '{"name":"app","require":%s},' % deps

    for pod in resultList:
        if len(pod.dependencies) > 0:
            podDeps = generate_json_deps(pod.dependencies)
            json += '{"name":"%s","require":%s},' % (pod.name, podDeps)
        else:
            json += '{"name":"%s","require":{}},' % pod.name

    return json[:len(json)-1] + ']}'

def save_json_file(data, fileName):
    with open(fileName + '.json', 'w') as outfile:  
        outfile.write(generate_json(data))

def save_html_wheel_file(data, fileName):
    P_TEMPLATE = '<html><head> <title>deps</title> <meta charset="utf-8"> <style>.dependencyWheel{font: 10px sans-serif;}</style></head><body> <center> <div class="container"> <div id="chart_placeholder"></div><script src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.13.0/d3.min.js"></script> <script>d3.chart=d3.chart||{},d3.chart.dependencyWheel=function(e){var t=window,r=document,n=r.documentElement,a=r.getElementsByTagName("body")[0],c=(t.innerWidth||n.clientWidth||a.clientWidth,t.innerHeight||n.clientHeight||a.clientHeight,200),i=.03,o=960;function u(e){e.each(function(e){var t=e.matrix,r=e.packageNames,n=o/2-c,a=d3.chord().padAngle(i).sortSubgroups(d3.descending),u=d3.select(this).selectAll("svg").data([e]).enter().append("svg:svg").attr("width",o).attr("height",o).attr("class","dependencyWheel").append("g").attr("transform","translate("+o/2+","+o/2+")"),d=d3.arc().innerRadius(n).outerRadius(n+20),l=function(e){return 0===e.index?"#ccc":"hsl("+parseInt((r[e.index][0].charCodeAt()-97)/26*360,10)+",90%,70%)"},s=function(e){return function(t,r){u.selectAll(".chord").filter(function(e){return e.source.index!=r&&e.target.index!=r}).transition().style("opacity",e);var n=[];u.selectAll(".chord").filter(function(e){e.source.index==r&&n.push(e.target.index),e.target.index==r&&n.push(e.source.index)}),n.push(r);var a=n.length;u.selectAll(".group").filter(function(e){for(var t=0;t<a;t++)if(n[t]==e.index)return!1;return!0}).transition().style("opacity",e)}},g=a(t),p=g.groups[0],h=-(p.endAngle-p.startAngle)/2*(180/Math.PI),f=u.selectAll("g.group").data(g.groups).enter().append("svg:g").attr("class","group").attr("transform",function(e){return"rotate("+h+")"});f.append("svg:path").style("fill",l).style("stroke",l).attr("d",d).style("cursor","pointer").on("mouseover",s(.1)).on("mouseout",s(1)),f.append("svg:text").each(function(e){e.angle=(e.startAngle+e.endAngle)/2}).attr("dy",".35em").attr("text-anchor",function(e){return e.angle>Math.PI?"end":null}).attr("transform",function(e){return"rotate("+(180*e.angle/Math.PI-90)+")translate("+(n+26)+")"+(e.angle>Math.PI?"rotate(180)":"")}).style("cursor","pointer").text(function(e){return r[e.index]}).on("mouseover",s(.1)).on("mouseout",s(1)),u.selectAll("path.chord").data(g).enter().append("svg:path").attr("class","chord").style("stroke",function(e){return d3.rgb(l(e.source)).darker()}).style("fill",function(e){return l(e.source)}).attr("d",d3.ribbon().radius(n)).attr("transform",function(e){return"rotate("+h+")"}).style("opacity",1)})}return u.width=function(e){return arguments.length?(o=e,u):o},u.margin=function(e){return arguments.length?(c=e,u):c},u.padding=function(e){return arguments.length?(i=e,u):i},u};var buildMatrixFromDependencies=function(e){var t=e.packages,r={},n={},a=[],c=0,i={};return t.forEach(function(e){if(e.replace)for(replaced in e.replace)i[replaced]=e.name}),t.forEach(function(e){for(packageName in e.require)packageName in i&&(e.require[i[packageName]]=e.require[packageName],delete e.require[packageName])}),t.forEach(function(e){packageName=e.name,packageName in r||(n[c]=packageName,r[packageName]=c++)}),t.forEach(function(e){var t=r[e.name],n=a[t];if(!n){n=a[t]=[];for(var i=-1;++i<c;)n[i]=0}for(packageName in e.require)n[r[packageName]]++}),a.forEach(function(e,t){for(var r=.001,n=-1;++n<c;){var a=(n+t)%c;1==e[a]&&(e[a]+=r,r+=.001)}}),{matrix:a,packageNames:n}};d3.select("#chart_placeholder svg").remove(),d3.select("#chart_placeholder").datum(buildMatrixFromDependencies(JSON.parse(P_DATA_JSON))).call(d3.chart.dependencyWheel().width(P_DATA_WIDTH).margin(P_DATA_MARGIN).padding(P_DATA_PADDING));</script> </div></center></body></html>'
    P_DATA_JSON = "'%s'" % generate_json(data)
    P_DATA_WIDTH = "960"
    P_DATA_MARGIN = "200"
    P_DATA_PADDING = ".02"

    html_out = P_TEMPLATE.replace("P_DATA_JSON", P_DATA_JSON).replace("P_DATA_WIDTH", P_DATA_WIDTH).replace("P_DATA_MARGIN", P_DATA_MARGIN).replace("P_DATA_PADDING", P_DATA_PADDING)

    with open(fileName + '.html', 'w') as outfile:  
        outfile.write(html_out)

def main():
    if len(sys.argv) == 1:
        print "%s - %s (%s)\nby %s\n" % (PROJECT_NAME, __version__, PROJECT_DESCRIPTION, PROJECT_AUTHOR)
        print "type: -h to see more information"
        sys.exit(1)

    parser = OptionParser("usage: %prog [options] filename")
    parser.add_option("-f", "--file", dest="file", default="", type="string", help="specify file path")
    parser.add_option("--show", action='store_true', dest="show", help="print dependencies on console")
    parser.add_option("--json", action='store_true', dest="json", help="save dependencies to json file")
    parser.add_option("--html", action='store_true', dest="html", help="save dependencies to wheel graph html file")        
    (options, args) = parser.parse_args()

    if len(options.file) != 0:

        if options.show != True and options.json != True and options.html != True:
            print "you must select an output option (show | json | html)\n"
            sys.exit(1)

        if ".lock" not in options.file:
            options.file += ".lock"

        result = parse_lock_file(options.file)

        if options.show:
            print "Printing dependencies..."
            for pod in result:
                pod.printObject()

        if options.json:
            print "Saving json file..."
            save_json_file(result, options.file)

        if options.html:
            print "Saving html file..."
            save_html_wheel_file(result, options.file)

        print "done"
