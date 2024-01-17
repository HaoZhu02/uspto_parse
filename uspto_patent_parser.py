from parser_txt import *
from parser_xml_2 import *
from parser_xml_4 import *
import time
import re


# Parse from online
def read_and_parse_from_url(url,data_items):
        m = re.search('(?<=fulltext/)\d+', url)
        year = int(m.group(0))
        full_yearly_data = []
        if year <= 2001:
            raw_patent_data = read_data_from_url_txt(url)
            for patent in raw_patent_data:
                if 'URL' in data_items:
                    full_yearly_data.append(parse_txt_patent_data(patent,source_url = url,data_items_list=data_items))
                else:
                    full_yearly_data.append(parse_txt_patent_data(patent,data_items_list=data_items))
        elif year in [2002,2003,2004]:
            raw_patent_data = read_data_from_url_xml_2(url)
            for patent in raw_patent_data:
                root_tree = ElementTree(fromstring(patent))
                if 'URL' in data_items:
                    full_yearly_data.append(parse_patent_data_xml_2(root_tree,source_url = url,data_items_list=data_items))
                else:
                    full_yearly_data.append(parse_patent_data_xml_2(root_tree,data_items_list=data_items))
        elif year > 2004:
            raw_patent_data = read_data_from_url_xml_4(url)
            for patent in raw_patent_data:
                root_tree = ElementTree(fromstring(patent))
                if 'URL' in data_items:
                    full_yearly_data.append(parse_patent_data_xml_4(root_tree,source_url = url,data_items_list=data_items))
                else:
                    full_yearly_data.append(parse_patent_data_xml_4(root_tree,data_items_list=data_items))
        return full_yearly_data


# Checks and prints the object structure
def print_object_structure(obj, indent=0):
    if isinstance(obj, (list, tuple)):
        print(f"{' ' * indent}List or Tuple:")
        for item in obj:
            print_object_structure(item, indent + 2)
    elif isinstance(obj, dict):
        print(f"{' ' * indent}Dictionary:")
        for key, value in obj.items():
            print(f"{' ' * (indent + 2)}Key: {key}")
            print_object_structure(value, indent + 4)
    else:
        print(f"{' ' * indent}{type(obj).__name__}")

# write into txt file
def write_to_txt(data, file, indent=0):
    for key, value in data.items():
        if isinstance(value, dict):
            file.write(f"{'  ' * indent}{filter_ascii(key)}:\n")
            write_to_txt(value, file, indent + 1)
        elif isinstance(value, (list, tuple)):
            file.write(f"{'  ' * indent}{filter_ascii(key)}:\n")
            for item in value:
                if isinstance(item, dict):
                    write_to_txt(item, file, indent + 1)
                else:
                    file.write(f"{'  ' * (indent + 1)}{filter_ascii(item)}\n")
        else:
            file.write(f"{'  ' * indent}{filter_ascii(key)}: {filter_ascii(value)}\n")

def filter_ascii(text):
    # Replace or omit non-ASCII characters
    return ''.join(char if 32 <= ord(char) <= 126 else ' ' for char in str(text))

def display_menu():
    print("\n1. Parse from web\n2. Quit")
    choice = input("\nEnter your choice: ")
    return choice

def get_date_input():
    year = input("Enter the year (YYYY): ")
    month = input("Enter the month (MM): ")
    day = input("Enter the day (DD): ")
    return year, month, day

def get_document_number():
    return input("Enter the target document number: ")

def construct_url(year, month, day):
    url = f'https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/{year}/ipg{year[2:]}{month}{day}.zip'
    return url


def main():
    while True:
        choice = display_menu()
        if choice == '1':
            items = ['INVT','ABST','DETD','CLMS']
            year, month, day = get_date_input()
            doc_number = get_document_number()
            url = construct_url(year, month, day)
            
            # Start timing
            start_time = time.time()

            # Process data
            data = read_and_parse_from_url(url, items)


            # Process data and write to file
            found_patent = None

            for patent_record in data:
                bibliographic_information = patent_record.get("bibliographic_information")
                if bibliographic_information and bibliographic_information.get("doc-number") == doc_number:
                    found_patent = patent_record
                    break

            file_path = f'patent_info{doc_number}.txt'

            # Write data to file
            with open(file_path, 'w', encoding='utf-8') as file:
                write_to_txt(found_patent, file)

            print(f"\nData has been successfully written to {file_path}")

            # Record time
            end_time = time.time()  # End time recording
            total_time = end_time - start_time  # Calculate total time
            print(f"Total time taken: {total_time:.2f} seconds")

        elif choice == '2':
            print("\nExiting program.\n")
            break
        else:
            print("\nInvalid choice. Please try again.\n")

    
if __name__ == "__main__":
    main()