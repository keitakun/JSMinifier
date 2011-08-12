#################################################################################
#	 JSMinifier.py - Merge and compress JS files
#    Copyright (C) <2011>  <keita kuroki: keita@hellokeita.in>
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

#!/usr/bin/env python
import os
import re
import sys
import tempfile

from optparse import OptionParser

parser = OptionParser();
parser.add_option("-o", "--output", dest="outputFile");
parser.add_option("-p", "--path", dest="path");

(options, args) = parser.parse_args();

if (options.outputFile == None): sys.exit("Please set the -o or --output parameter.");
if (options.path == None): sys.exit("Please set the -p or --path parameter.");

def listDir(path, fileType = "*"):
	files = os.listdir(path);
	filteredFiles = [];
	ftRE = re.compile(r"\." + fileType + "$", re.I);
	for f in files:
		if(os.path.isdir(path + "/" + f)):
			filteredFiles.extend(listDir(path + "/" + f, fileType));
		else:
			if ftRE.search(f):
				filteredFiles.append(path + "/" + f);
	return filteredFiles;

def concatJS(files):
	output = "";
	for p in files:
		f = open(p, "r");
		output += "// FILE: " + p + "\n";
		output += f.read();
		output += "\n// END OF FILE: " + p + "\n";
		output += "\n\n";
		f.close();
	return output;

def compress(text):

	in_tuple = tempfile.mkstemp()
	with os.fdopen(in_tuple[0], 'w') as handle:
		handle.write(text)

	out_tuple = tempfile.mkstemp()

	os.system("java -jar compiler/compiler.jar --language_in=ECMASCRIPT5_STRICT --js %s --js_output_file %s" % (in_tuple[1], out_tuple[1]))

	with os.fdopen(out_tuple[0], 'r') as handle:
		compressed = handle.read()

	os.unlink(in_tuple[1])
	os.unlink(out_tuple[1])

	return compressed

files = listDir(options.path, "js");
out = concatJS(files);
out = compress(out);

f = open(options.outputFile, "w+");
f.write(out);
f.close();
