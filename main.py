import os
import shutil

import builders

in_path = "src"
out_path = "out"

for walk_result in os.walk(in_path):
    # Get the output version of the path
    this_in_path = walk_result[0]
    this_out_path = walk_result[0].replace(in_path, out_path, 1)

    # Make the folder if it doesn't exist
    if not os.path.exists(this_out_path):
        os.mkdir(this_out_path)

    for file in walk_result[2]:
        in_file = os.path.join(this_in_path, file)
        out_file = os.path.join(this_out_path, file).removesuffix(".buildme")  # Remove from the output if it is there

        if in_file.endswith(".buildme"):  # If this needs to be built then read it in and out
            # Read it in, select the builder, build it, and then write it
            builder_name, contents = open(in_file, "r").read().split("\n", 1)
            new_data = builders.builders[builder_name].build(contents)
            open(out_file, "w").write(new_data)


        else:  # Otherwise just copy the file
            shutil.copyfile(in_file, out_file)
