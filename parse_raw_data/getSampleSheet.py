import os
import sys

# Get your Current Working Directory
path = sys.argv[1]

# Get a list of all of the files (and directories, if there are any) in your directory.
# This will be a list of strings.
filenames = os.listdir(path)

# Split each one into the chunks that were separated by underscores ("_") and then keep the first three for each name.
# This will be a list of lists.
chunked_names = [filename.split("_")[0:3] for filename in filenames if filename.endswith(".idat")]
# print(chunked_names)

# For each name, rejoin the three chunks with commas
# We're back to having a list of strings.
csv_lines = [",".join(chunks) for chunks in chunked_names]
# Join all of those strings with the newline character to get just a long string.
contents = "\n".join(csv_lines)

# Print this string to standard output so that it can be redirected to a file.

print(contents)