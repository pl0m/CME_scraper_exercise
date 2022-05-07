import time
from selenium.webdriver.common.by import By

from scraper_futures_utils import Utils


def scrape_futures_settlements():
    utils = Utils()
    
    time.sleep(2)
    utils.navigate('https://www.cmegroup.com/markets/energy/refined-products/singapore-gasoil-swap-futures.settlements.html')
    
    time.sleep(3)
    
    utils.click_deny_cookies()

    table_rows_before = utils.find_elements('tbody tr')
    table_row_count_before = len(table_rows_before)

    time.sleep(1)

    utils.click_load_all()
    
    time.sleep(1)

    print("Ready to fetch table")
    
    # Get all table header row elements
    table_header_elements = utils.find_elements('thead tr')
    # Get all table header columns for each row and combine them with comma
    table_headers = [','.join([str(th.text.replace("\n", '')) for th in tr.find_elements(By.CSS_SELECTOR, 'th')]) for tr in table_header_elements]

    # The second row contains the first column header
    header_first_column_row = table_headers[1]
    # Split the first row by comma and get the first column
    header_first_column = header_first_column_row.split(",")[0]
    # The first row contains all the other column headers
    header_other_columns = table_headers[0]
    # Prepend the first column to the other columns and store as variable
    table_headers_csv = header_first_column + header_other_columns

    print(table_headers_csv)

    table_row_elements = utils.find_elements('tbody tr')
    table_rows = [','.join([str(td.text.replace("\n", '')) for td in tr.find_elements(By.CSS_SELECTOR, 'td')]) for tr in table_row_elements]
    
    # Number of rows before "load all"
    upper_count = int(table_row_count_before / 2)
    # Number of rows after "load all"
    middle_count = int((len(table_row_elements) - table_row_count_before) / 2)
    # Position at the end of the rows after "load all" and before the first-column-rows of the rows before "load all"
    middle = upper_count + middle_count

    # Rows before "load all" but without first column
    rows_upper_right = table_rows[0 : upper_count]
    # Rows after "load all", completely
    rows_middle = table_rows[upper_count : middle]
    # Rows before "load all" but only first column
    rows_upper_left = table_rows[middle : middle + upper_count]

    # Create empty list to store final rows
    table_rows_final = []

    # Count from 0 to upper_count
    for row_index in range(upper_count):
        # Get the row with only the first column by using the counter
        row_first_column_row = rows_upper_left[row_index]
        # Split the first row by comma and get the first column
        row_first_column = row_first_column_row.split(",")[0]
        # Get the row with the other columns by using the counter
        other_columns = rows_upper_right[row_index]
        # Prepend the first column to the other columns and store as variable
        row_final_row = row_first_column + other_columns
        # Add the final row to the list of final rows (to be saved later)
        table_rows_final.append(row_final_row)
    
    # Add the rows after "load all" to the final rows list
    table_rows_final.extend(rows_middle)

    # Turn the final rows list into "\n" (line break) separated text
    table_rows_csv = "\n".join(table_rows_final)
    print(table_rows_csv)
    
    table_csv = table_headers_csv + "\n" + table_rows_csv
    utils.save_to_storage('settlements', table_csv)