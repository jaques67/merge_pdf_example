# Combine PDFs

A simple example of reading all PDF files in folder supplied on the command line.  
It then reads an exclusion file, if it exists, and removes those PDF files from processing.  
Finally, all the PDF documents are merged into one PDF document.  

```` shell
Usage:
    python combine_pdfs.py -id <input_directory> -o <output_file>

Arguments:
    -id, --input_directory: The directory containing the PDF files to combine.
    -o, --output_file: The name of the combined PDF output file.
    -od, --output_directory: Optional. The directory where the combined PDF is saved.
    -v, --verbosity: Optional. Increase verbosity.
````
