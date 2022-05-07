import datetime
import time
from scraper_futures_utils import Utils
from selenium.webdriver.common.by import By

def scrape_futures_quotes():
    # Table header as fetched by selenium
    #
    # -------------------------------------------------------------------------------------------------
    # |       | OPTIONS | CHART | LAST | CHANGE | PRIOR SETTLE | OPEN | HIGH | LOW | VOLUME | UPDATED |
    # -------------------------------------------------------------------------------------------------
    # | MONTH |         |       |      |        |              |      |      |     |        |         |
    # -------------------------------------------------------------------------------------------------
    utils = Utils()

    utils.navigate('https://www.cmegroup.com/markets/energy/refined-products/singapore-gasoil-swap-futures.quotes.html')
    
    time.sleep(1)
    button = utils.find_element('.load-all')
    utils.move_to_element(button)
    
    utils.find_element('#onetrust-reject-all-handler').click()
    
    time.sleep(1)
    button.click()
    
    # FIXME: Temporary hack to "get" table headers because structure is messed up
    table_headers_csv = 'MONTH,OPTIONS,CHART,LAST,CHANGE,PRIOR SETTLE,OPEN,HIGH,LOW,VOLUME,UPDATED'
    
    table_rows = utils.find_elements('.table-row-animate')
    #table_rows2 = "\n".join([','.join([str(td.text.replace("\n", '')) for td in tr.find_elements(By.CSS_SELECTOR, 'td')]) for tr in table_rows])[1:]
    table_rows_csv_array = []
    table_rows_csv = ""
    
    # Row count to half of total row count because of the split table structure
    # Then we can check in which half of the data we are
    row_count = len(table_rows) / 2
    print("Rows: " + str(row_count))
    
    counter = 0

   
    # TODO replace block with function call 
    for tr in table_rows:
        if(counter < row_count): # First part of data (everything except "MONTH")
            specialColumns = 2
            row_csv = ''
            # Find all cells
            for td in tr.find_elements(By.CSS_SELECTOR, 'td'):
                # If first element do nothing, else add ',' at the beginning
                if specialColumns > 0:
                    specialColumns -= 1
                    # Skip the very first column because it's empty
                    if specialColumns == 1:
                        continue
                else:
                    row_csv += ','
                
                # Add cell content to row csv contents
                row_csv += str(td.text.replace("\n", ' '))
            # Add row to list
            table_rows_csv_array.append(row_csv)
        else: # Second part of data ("MONTH" only)
            # Get and remove first row from list
            row_csv = table_rows_csv_array.pop(0)
            # Get "month" cell contents
            month_cell_content = tr.find_element(By.CSS_SELECTOR, 'td').text.replace("\n", ' ')
            # Create the row contents
            row_csv = month_cell_content + ',' + row_csv
            # Add row content and line break to csv
            table_rows_csv += row_csv + "\n"
        counter += 1
    
    print(table_rows_csv)
    
    table_csv = table_headers_csv + "\n" + table_rows_csv
    utils.save_to_storage('quotes', table_csv)
    