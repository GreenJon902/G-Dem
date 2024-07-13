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

    # Process each file that we found
    for file in walk_result[2]:
        in_file = os.path.join(this_in_path, file)

        print(f"Processing file \"{in_file}\"")

        if in_file.endswith(".buildme"):  # If this needs to be built then read it in and out

            # Create a path for the builder.
            path_for_builder = in_file.removeprefix(in_path).lstrip("/").removesuffix(".buildme")

            # Read it in, select the builder, get the result from the builder
            builder_name, contents = open(in_file, "r").read().split("\n", 1)
            builder = builders.builders[builder_name]
            built_files = builder.build(path_for_builder, contents)

            # Write each built file to the correct place
            for built_file in built_files:
                open(os.path.join(out_path, built_file.file_path), "w").write(built_file.file_contents)


        else:  # Otherwise just copy the file
            out_file = os.path.join(this_out_path, file)
            shutil.copyfile(in_file, out_file)
