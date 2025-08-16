#!/usr/bin/env fish

function patch_fonts
    # Define keyword arguments
    argparse 'f/factor=' h/help -- $argv
    or return

    # Show help if requested or no arguments provided
    if set -q _flag_help; or test (count $argv) -eq 0
        echo "Usage: patch_fonts [OPTIONS] <font_file_or_glob>"
        echo ""
        echo "Options:"
        echo "  -f, --factor VALUE    Line height factor (default: 1.3)"
        echo "  -h, --help           Show this help message"
        echo ""
        echo "Examples:"
        echo "  patch_fonts fonts/OperatorMono/OperatorMono-Bold.ttf"
        echo "    # Patches a single font file"
        echo ""
        echo "  patch_fonts 'fonts/OperatorMono/*.ttf'"
        echo "    # Patches all TTF files in directory (use quotes for glob)"
        echo ""
        echo "  patch_fonts --factor 1.5 'fonts/**/*.otf'"
        echo "    # Patches all OTF files recursively with 1.5x line height"
        echo ""
        echo "  patch_fonts -f 1.2 ~/Downloads/JetBrainsMono-*.ttf"
        echo "    # Patches matching JetBrains Mono files"
        return 0
    end

    # Set default for factor if not provided
    set -l factor (set -q _flag_factor; and echo $_flag_factor; or echo "1.3")

    # Expand the glob pattern or single file
    set -l font_files
    for pattern in $argv
        set -a font_files (eval "echo $pattern")
    end

    # Check if any files were found
    if test (count $font_files) -eq 0
        echo "Error: No files found matching pattern '$argv'"
        return 1
    end

    # Validate all are files
    for file in $font_files
        if not test -f $file
            echo "Error: '$file' is not a valid file"
            return 1
        end
    end

    echo "Line height factor: $factor"
    echo "Found "(count $font_files)" font file(s) to patch"
    echo ""

    # Process each font file
    for font_file in $font_files
        set -l font_file_abs (realpath $font_file)
        set -l font_dir (dirname $font_file_abs)
        set -l font_name (basename $font_file_abs)

        echo "Processing: $font_file"
        docker run --rm -v $font_dir:/home font-patcher \
            python3 /app/main.py \
            --factor=$factor \
            --input=/home/$font_name \
            --outputDir=/home
    end

    echo ""
    echo "✓ Font patching complete!"
end
