import argparse
import fontforge
from pathlib import Path
from termcolor import colored


def parse_opts() -> dict:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Adjust font line height and other metrics'
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to the input font file'
    )

    parser.add_argument(
        '--outputDir', '-o',
        default='.',
        help='Output directory for the patched font (default: current directory)'
    )

    parser.add_argument(
        '--factor', '-f',
        type=float,
        default=1.3,
        help='Factor to adjust the font metrics (default: 1.3)'
    )

    parser.add_argument(
        '--fontname',
        default=None,
        help='Override the fontname (default: append factor to original)'
    )

    parser.add_argument(
        '--familyname',
        default=None,
        help='Override the family name (default: append factor to original)'
    )

    parser.add_argument(
        '--fullname',
        default=None,
        help='Override the full name (default: append factor to original)'
    )

    args = parser.parse_args()
    return vars(args)  # Convert to dictionary


def adjust(font, attribute: str, factor: float) -> None:
    """Adjust an attribute of a font by a given factor."""
    original = getattr(font, attribute)
    new = int(getattr(font, attribute) * factor)

    print(f"Adjusting {colored(attribute, 'yellow', attrs=['bold'])}: "
          f"{colored(original, 'red')} -> {colored(new, 'green')}")
    setattr(font, attribute, new)


def main() -> None:
    args = parse_opts()
    font = fontforge.open(args["input"])

    print('')

    # Adjust ascent properties
    for prop in ['os2_winascent', 'os2_typoascent', 'hhea_ascent']:
        adjust(font, prop, args["factor"])

    # Adjust descent properties
    for prop in ['os2_windescent', 'os2_typodescent', 'hhea_descent']:
        adjust(font, prop, args["factor"] * 2)

    # Set font names
    for attr in ['fontname', 'familyname', 'fullname']:
        value = args[attr] or f"{getattr(font, attr)} {args['factor']}"
        setattr(font, attr, value)

    # Prepare output filename
    input_path = Path(args["input"])
    filename = input_path.stem
    extension = input_path.suffix
    new_filename = f"{filename}Patched {args['factor']}{extension}"

    print('')
    print(colored('Successfully created patched font:', 'green'))
    print(f"{colored('                         Fontname: ', 'white', attrs=['bold'])}"
          f"{colored(font.fontname, 'blue')}")
    print(f"{colored('                      Family Name: ', 'white', attrs=['bold'])}"
          f"{colored(font.familyname, 'blue')}")
    print(f"{colored('                  Name for Humans: ', 'white', attrs=['bold'])}"
          f"{colored(font.fullname, 'blue')}")
    print('')

    # Update SFNT names
    sfnt = {el[1]: el for el in font.sfnt_names}
    sfnt["UniqueID"] = ('English (US)', 'UniqueID', font.fontname)
    sfnt["Preferred Family"] = ('English (US)', 'Preferred Family', font.familyname)
    font.sfnt_names = tuple(sfnt.values())

    # Save the font
    output_path = Path(args["outputDir"]) / new_filename
    font.save(str(output_path))
    font.generate(str(output_path))

    print(colored(f'Saved patched font file: {colored(new_filename, "blue")}', 'green'))


if __name__ == "__main__":
    main()
