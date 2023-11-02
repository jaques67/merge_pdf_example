"""
This program combines multiple PDF files into a single PDF.

It takes PDF files from the input directory, combines them, and
saves the combined PDF to the output file or directory.

Usage:
    python combine_pdfs.py -id <input_directory> -o <output_file>

Arguments:
    -id, --input_directory: The directory containing the PDF files to combine.
    -o, --output_file: The name of the combined PDF output file.
    -od, --output_directory: Optional. The directory where the combined PDF is saved.
    -v, --verbosity: Optional. Increase verbosity.

Author: Jaques Strydom
"""
import sys

import PyPDF2
import argparse
import os
import glob


def argument_parser():
    """
    Check that the required parameters have been passed in from the command line.

    :return: Returns the parser arguments.
    """
    parser = argparse.ArgumentParser()
    # Required argument
    parser.add_argument("-id", "--input_directory", required=True, type=str,
                        help="Specify the directory containing the PDF files to combine")
    # Optional argument
    parser.add_argument("-od", "--output_directory", type=str,
                        help="Specify the combined PDF output directory")
    parser.add_argument('-o', '--output_file', type=str,
                        help="Specify the output file name")
    parser.add_argument("-v", "--verbosity", action="store_true", help="Increase verbosity")

    return parser.parse_args()


def validate_folder(directory):
    """
    Verify that the folder passed in by the user exists

    :param directory:
    :return: Returns True if the folder/directory exists or False if it does not.
    """

    if os.path.exists(directory):
        return True

    return False


def exclude_files(pdf_list, filename):
    """
    Read the exclusion text file and remove all of those names from the PDF list
    :param pdf_list: List containing all the PDF names to combine
    :param filename: File to be processed to find list of excluded PDFs
    :return: None
    """
    global verbosity

    if not os.path.exists(filename):
        return

    if verbosity:
        print("Retrieve exclude files.")

    with open(filename, mode='r') as f:
        contents = f.readlines()

    for file in contents:
        stripped_filename = file.rstrip('\n')
        if stripped_filename in pdf_list:
            if verbosity:
                print(f"Excluding {stripped_filename}")
            pdf_list.remove(stripped_filename)


def fetch_pdf_list(directory):
    """
    Retrieve a list of all the PDF documents in the folder with the path
    stripped from the name.

    :param directory: Directory containing all the PDF files
    :return: A list of strings containing the PDF file names
    """
    global verbosity

    pdf_files = glob.glob(os.path.join(directory, '*.pdf'))
    # Extract only file names
    pdf_file_names = [os.path.basename(pdf_file) for pdf_file in pdf_files]

    return pdf_file_names


def build_outputfile(input_dir, output_dir, filename):
    """
    Create the output file name depending on whether an output directory was specified.
    :param input_dir: Folder containing all the PDF documents for processing
    :param output_dir: Optional folder where to write the combined output file to
    :param filename: The filename specified by the user
    :return: We return the full path of the output file, i.e. name and directory
    """
    global verbosity

    if output_dir:
        out_file = os.path.join(output_dir, filename)
    else:
        out_file = os.path.join(input_dir, filename)

    # Delete file if it exists
    try:
        if os.path.exists(out_file):
            if verbosity:
                print(f"Removing output file: {out_file}")
            os.remove(out_file)
    except PermissionError:
        print(f"File {out_file} could not be deleted!")

    return out_file


def combine_pdfs(pdf_list, directory, output_file):
    """
    Merge all PDF documents supplied into a single output PDF and
    save the file as output_file
    :param pdf_list: List of filenames
    :param directory: folder containing the PDFs
    :param output_file: Directory and output PDF name of file created
    :return: None
    """
    global verbosity

    print("Combining PDFs")
    pdf_merger = PyPDF2.PdfFileMerger()

    for pdf in pdf_list:
        if verbosity:
            print(f"adding file: {pdf}")
        input_file = os.path.join(directory, pdf)
        pdf_merger.append(input_file)

    try:
        print('Writing combined PDF')
        with open(output_file, 'wb') as output_file:
            pdf_merger.write(output_file)
    except PermissionError:
        print(f'Failed to open output file {output_file} for writing.')
        raise
    finally:
        pdf_merger.close()


def main():
    global verbosity

    all_pdfs = []
    args = argument_parser()
    verbosity = args.verbosity

    output_file = build_outputfile(args.input_directory, args.output_directory, args.output_file)

    if not validate_folder(args.input_directory):
        sys.exit()

    all_pdfs.extend(fetch_pdf_list(args.input_directory))
    exclude_files(all_pdfs, filename='exclusion.txt')

    if args.output_file in all_pdfs:
        all_pdfs.remove(args.output_file)
        print('output file deleted from list')

    all_pdfs.sort()

    combine_pdfs(all_pdfs, args.input_directory, output_file)


if __name__ == '__main__':
    verbosity = False

    print("Program start")
    main()
    print("Processing complete!")

